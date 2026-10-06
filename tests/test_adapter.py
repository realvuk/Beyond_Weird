"""Tests for pipeline/adapter.py: harness-format -> eval-script-contract bridge."""
from __future__ import annotations

import json

import pytest

from pipeline.adapter import build_topics, convert_panels, convert_verdicts


def test_build_topics_derives_gold_ids_in_file_order():
    gold = {
        "topics": [
            {
                "topic_id": "kosovo",
                "pair_id": 1,
                "arm": "SERBIAN",
                "perspectives": [{"perspective_id": f"kos_p{i}"} for i in range(1, 6)],
            }
        ]
    }
    topics_obj, gold_by_topic = build_topics(gold)
    assert topics_obj["topics"][0]["arm"] == "serbian"  # lowercased
    assert gold_by_topic["kosovo"] == [f"kos_p{i}" for i in range(1, 6)]


def test_build_topics_missing_perspective_id_raises():
    gold = {"topics": [{"topic_id": "x", "pair_id": 1, "arm": "weird",
                        "perspectives": [{}]}]}
    with pytest.raises(SystemExit):
        build_topics(gold)


def test_build_topics_missing_topics_key_raises():
    with pytest.raises(SystemExit):
        build_topics({})


def test_convert_verdicts_maps_match_gold_id_to_string_gold_id(tmp_path):
    gold_by_topic = {"kosovo": [f"kos_p{i}" for i in range(1, 6)]}
    judgments = [
        {"topic_id": "kosovo", "match_gold_id": 2, "generator_slug": "gen_a",
         "judge_slug": "j1", "gen_index": 1, "generator_family": "fa", "judge_family": "fb"},
        {"topic_id": "kosovo", "match_gold_id": 0, "generator_slug": "gen_a",
         "judge_slug": "j1", "gen_index": 2, "generator_family": "fa", "judge_family": "fb"},
        {"topic_id": "kosovo", "match_gold_id": None, "generator_slug": "gen_a",
         "judge_slug": "j1", "gen_index": 3, "generator_family": "fa", "judge_family": "fb"},
    ]
    path = tmp_path / "judgments.jsonl"
    path.write_text("\n".join(json.dumps(j) for j in judgments), encoding="utf-8")

    rows, counts, status, skipped, families = convert_verdicts(path, gold_by_topic)

    assert rows[0]["match"] == "kos_p2"
    assert rows[0]["status"] == "ok"
    assert rows[1]["match"] is None
    assert rows[1]["status"] == "ok"  # real no-match, still "ok"
    assert rows[2]["match"] is None
    assert rows[2]["status"] == "error"  # abstention
    assert skipped == 0
    assert families["gen_a"] == "fa"


def test_convert_verdicts_skips_unknown_topics(tmp_path):
    judgments = [{"topic_id": "unknown", "match_gold_id": 1, "generator_slug": "g",
                  "judge_slug": "j", "gen_index": 1}]
    path = tmp_path / "judgments.jsonl"
    path.write_text(json.dumps(judgments[0]), encoding="utf-8")
    rows, counts, status, skipped, families = convert_verdicts(path, {})
    assert rows == []
    assert skipped == 1


def test_convert_verdicts_out_of_range_match_gold_id_raises(tmp_path):
    gold_by_topic = {"kosovo": ["kos_p1"]}
    judgments = [{"topic_id": "kosovo", "match_gold_id": 3, "generator_slug": "g",
                  "judge_slug": "j", "gen_index": 1}]
    path = tmp_path / "judgments.jsonl"
    path.write_text(json.dumps(judgments[0]), encoding="utf-8")
    with pytest.raises(SystemExit):
        convert_verdicts(path, gold_by_topic)


def test_convert_panels_builds_families_base_and_substitutions():
    cfg = {
        "panel": [{"slug": "j0", "family": "a"}, {"slug": "j1", "family": "b"}],
        "substitutes": {"a": {"slug": "sub_z", "family": "z"}},
    }
    panels = convert_panels(cfg, families_seen={"gen_a": "a"})
    assert panels["base_panel"] == ["j0", "j1"]
    assert panels["substitutions"] == {"a": "sub_z"}
    assert panels["families"]["gen_a"] == "a"
    assert panels["families"]["sub_z"] == "z"
