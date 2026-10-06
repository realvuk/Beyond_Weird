"""Tests for bweird.parsing: LLM output -> typed dataclass parsing."""
from __future__ import annotations

import pytest

from bweird.errors import ParseError
from bweird.parsing import extract_json_value, parse_judgment, parse_perspectives


def test_extract_json_value_plain():
    assert extract_json_value('{"a": 1}') == {"a": 1}


def test_extract_json_value_fenced():
    text = 'here you go:\n```json\n{"a": 1}\n```'
    assert extract_json_value(text) == {"a": 1}


def test_extract_json_value_embedded_in_prose():
    text = 'Sure, here is the result: {"a": 1} — hope that helps!'
    assert extract_json_value(text) == {"a": 1}


def test_extract_json_value_empty_raises():
    with pytest.raises(ParseError):
        extract_json_value("   ")


def test_extract_json_value_no_json_raises():
    with pytest.raises(ParseError):
        extract_json_value("no json here at all")


def test_parse_perspectives_happy_path():
    text = 'noise\n```json\n[{"summary": "s", "explanation": "e"}]\n```'
    result = parse_perspectives(text)
    assert result[0].summary == "s"
    assert result[0].index == 1


def test_parse_perspectives_wrapped_in_object():
    text = '{"perspectives": [{"summary": "s", "explanation": "e"}]}'
    assert parse_perspectives(text)[0].summary == "s"


def test_parse_perspectives_empty_list_raises():
    with pytest.raises(ParseError):
        parse_perspectives("[]")


def test_parse_perspectives_too_many_raises():
    items = [{"summary": "s", "explanation": "e"}] * 6
    import json
    with pytest.raises(ParseError):
        parse_perspectives(json.dumps(items))


def test_parse_perspectives_missing_summary_raises():
    with pytest.raises(ParseError):
        parse_perspectives('[{"explanation": "e"}]')


def test_parse_judgment_happy_path():
    judgment = parse_judgment('{"match": 3, "scope_ok": true, "reason": "r"}', n_gold=5)
    assert judgment.match == 3
    assert judgment.scope_ok is True


def test_parse_judgment_string_attributes_coerced_to_tuple():
    judgment = parse_judgment(
        '{"match": 3, "scope_ok": true, "reason": "r", "attributes": "single stance"}',
        n_gold=5,
    )
    assert judgment.attributes == ("single stance",)


def test_parse_judgment_list_attributes():
    judgment = parse_judgment(
        '{"match": 3, "scope_ok": true, "reason": "r", "attributes": ["a", "b"]}',
        n_gold=5,
    )
    assert judgment.attributes == ("a", "b")


def test_parse_judgment_invalid_attributes_type_raises():
    with pytest.raises(ParseError):
        parse_judgment(
            '{"match": 3, "scope_ok": true, "reason": "r", "attributes": 123}', n_gold=5
        )


def test_parse_judgment_out_of_range_match_raises():
    with pytest.raises(ParseError):
        parse_judgment('{"match": 6, "scope_ok": true, "reason": "r"}', n_gold=5)


def test_parse_judgment_no_match_is_zero_and_valid():
    judgment = parse_judgment('{"match": 0, "scope_ok": true, "reason": "r"}', n_gold=5)
    assert judgment.match == 0


def test_parse_judgment_bool_match_rejected():
    # bool is a subclass of int in Python; must be rejected explicitly.
    with pytest.raises(ParseError):
        parse_judgment('{"match": true, "scope_ok": true, "reason": "r"}', n_gold=5)


def test_parse_judgment_missing_reason_raises():
    with pytest.raises(ParseError):
        parse_judgment('{"match": 1, "scope_ok": true}', n_gold=5)
