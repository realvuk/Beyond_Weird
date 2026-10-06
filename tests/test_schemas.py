"""Tests for bweird.schemas: typed data model and topic-instrument loading."""
from __future__ import annotations

import json

import pytest

from bweird.errors import DataError
from bweird.schemas import (
    Arm,
    GeneratedPerspective,
    GenerationRecord,
    JudgeRole,
    JudgmentRecord,
    load_gold_standard,
    load_topics,
)


def test_generation_record_json_roundtrip():
    record = GenerationRecord(
        key="m::t",
        model_slug="m",
        model_family="fam",
        topic_id="t",
        perspectives=(GeneratedPerspective(index=1, summary="s", explanation="e"),),
        raw_response="raw",
        usage={"total_tokens": 7},
        created_at="2026-07-08T00:00:00+00:00",
    )
    back = GenerationRecord.from_json_dict(json.loads(json.dumps(record.to_json_dict())))
    assert back == record


def test_judgment_record_json_roundtrip_and_abstention():
    def judgment(match):
        return JudgmentRecord(
            key="m::t::p1::j1::panel",
            generator_slug="m",
            generator_family="fam",
            topic_id="t",
            gen_index=1,
            judge_slug="j1",
            judge_family="jf",
            role=JudgeRole.PANEL,
            presentation_order=(3, 1, 5, 2, 4),
            match_presented=match,
            match_gold_id=match,
        )

    matched = judgment(4)
    back = JudgmentRecord.from_json_dict(json.loads(json.dumps(matched.to_json_dict())))
    assert back == matched
    assert not matched.is_abstention
    assert judgment(None).is_abstention
    assert not judgment(0).is_abstention  # explicit no-match != abstention


def test_load_topics_valid():
    raw = [
        {"topic_id": "kosovo", "topic_title": "Kosovo", "population": "gen pop",
         "pair_id": "secession", "arm": "serbian"},
        {"topic_id": "quebec", "topic_title": "Quebec", "population": "gen pop",
         "pair_id": "secession", "arm": "weird"},
    ]
    topics = load_topics(raw)
    assert len(topics) == 2
    assert topics[0].arm == Arm.SERBIAN


def test_load_topics_empty_raises():
    with pytest.raises(DataError):
        load_topics([])


def test_load_topics_duplicate_topic_id_raises():
    raw = [
        {"topic_id": "x", "topic_title": "X", "population": "p",
         "pair_id": "pair1", "arm": "weird"},
        {"topic_id": "x", "topic_title": "X2", "population": "p",
         "pair_id": "pair2", "arm": "serbian"},
    ]
    with pytest.raises(DataError):
        load_topics(raw)


def test_load_topics_pair_missing_an_arm_raises():
    raw = [
        {"topic_id": "x", "topic_title": "X", "population": "p",
         "pair_id": "pair1", "arm": "weird"},
        {"topic_id": "y", "topic_title": "Y", "population": "p",
         "pair_id": "pair1", "arm": "weird"},  # same arm twice
    ]
    with pytest.raises(DataError):
        load_topics(raw)


def test_load_gold_standard_derives_gold_id_from_perspective_id_suffix():
    raw = {
        "topics": [
            {
                "topic_id": "kosovo",
                "perspectives": [
                    {"perspective_id": f"kos_p{i}", "summary": f"s{i}", "explanation": f"e{i}"}
                    for i in range(1, 6)
                ],
            }
        ]
    }
    gold = load_gold_standard(raw)
    assert [p.gold_id for p in gold["kosovo"]] == [1, 2, 3, 4, 5]


def test_load_gold_standard_wrong_count_raises():
    raw = {
        "topics": [
            {
                "topic_id": "kosovo",
                "perspectives": [
                    {"perspective_id": "kos_p1", "summary": "s", "explanation": "e"},
                ],
            }
        ]
    }
    with pytest.raises(DataError):
        load_gold_standard(raw)
