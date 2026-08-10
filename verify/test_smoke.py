#!/usr/bin/env python3
"""Minimal self-check for the pure-computation core: ``python test_smoke.py``.

No API calls, no fixtures, no framework -- just asserts over the pieces whose
breakage would silently corrupt results: record round-tripping, panel
substitution, the live credit-sum coverage rule, agreement coefficients,
bootstrap CIs, BH correction and JSON extraction.

Every assertion here targets code the pipeline actually runs. There is no
second aggregation implementation to drift against.
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

import pandas as pd

from bweird.analysis import (
    aggregate_model_topic,
    bh_correction,
    bootstrap_ci,
    cohen_kappa,
    fleiss_kappa,
    resolve_panel,
)
from bweird.config import JudgeConfig, ModelSpec
from bweird.errors import ParseError
from bweird.openrouter import _load_dotenv
from bweird.parsing import parse_judgment, parse_perspectives
from bweird.schemas import GeneratedPerspective, GenerationRecord, JudgeRole, JudgmentRecord


def _judgment(gen_index: int, judge: str, match: int | None) -> JudgmentRecord:
    """Build a minimal panel judgment record."""
    return JudgmentRecord(
        key=f"m::t::p{gen_index}::{judge}::panel",
        generator_slug="m",
        generator_family="fam",
        topic_id="t",
        gen_index=gen_index,
        judge_slug=judge,
        judge_family="jf",
        role=JudgeRole.PANEL,
        presentation_order=(3, 1, 5, 2, 4),
        match_presented=match,
        match_gold_id=match,
    )


def main() -> None:
    """Run all checks."""
    # Record round-trip through JSON (the actual checkpoint path).
    gen = GenerationRecord(
        key="m::t",
        model_slug="m",
        model_family="fam",
        topic_id="t",
        perspectives=(GeneratedPerspective(index=1, summary="s", explanation="e"),),
        raw_response="raw",
        usage={"total_tokens": 7},
        created_at="2026-07-08T00:00:00+00:00",
    )
    assert GenerationRecord.from_json_dict(json.loads(json.dumps(gen.to_json_dict()))) == gen

    jud = _judgment(1, "j1", 4)
    jud_back = JudgmentRecord.from_json_dict(json.loads(json.dumps(jud.to_json_dict())))
    assert jud_back == jud
    assert not jud.is_abstention and _judgment(1, "j1", None).is_abstention

    # Family-disjoint panel substitution.
    def spec(slug: str, family: str) -> ModelSpec:
        """Shorthand ModelSpec builder."""
        return ModelSpec(slug=f"{family}/{slug}", family=family, display_name=slug)

    config = JudgeConfig(
        base_panel=tuple(spec(f"j{i}", f) for i, f in enumerate("abcde")),
        substitutes={"a": spec("sub", "z")},
    )
    panel = config.build_panel("a")
    assert len(panel) == 5
    assert all(m.judge.family != "a" for m in panel)
    assert [m.substituted_for for m in panel] == ["a/j0", None, None, None, None]
    assert config.dropped_judge("a") == spec("j0", "a")
    assert config.dropped_judge("z") is None

    # The live credit-sum coverage rule (bweird.analysis.aggregate_model_topic).
    #
    # Hand-derivation of the expected numbers, so this test constrains the rule
    # rather than merely recording whatever it currently prints:
    #
    #   gen_1: j0,j1,j2 -> g2 ; j3 -> no-match ; j4 -> error (dropped)
    #   gen_2: j0,j1    -> g2 ; j2,j3,j4 -> no-match
    #   gen_3: everyone -> no-match
    #
    # Per-judge credit splits 1/k over the k generations that judge matched to
    # the same gold: j0 and j1 each matched g2 twice -> 1/2 per generation;
    # j2 matched g2 once -> 1; j3 and j4 never matched g2 -> 0.
    # A generation's weight is the mean of that credit over judges that RATED
    # it (j4 errored on gen_1, so gen_1's denominator is 4, not 5):
    #   gen_1 = (0.5 + 0.5 + 1 + 0) / 4 = 0.5
    #   gen_2 = (0.5 + 0.5 + 0 + 0 + 0) / 5 = 0.2
    #   gen_3 = 0
    # g2's credit for the model is the sum across generations = 0.7, and the
    # max rule takes the single best generation = 0.5.
    verdicts = pd.DataFrame(
        [
            {"judge": f"j{i}", "generation_id": "gen_1", "match": "g2", "status": "ok"}
            for i in range(3)
        ]
        + [
            {"judge": "j3", "generation_id": "gen_1", "match": None, "status": "ok"},
            {"judge": "j4", "generation_id": "gen_1", "match": None, "status": "error"},
        ]
        + [
            {"judge": f"j{i}", "generation_id": "gen_2", "match": "g2", "status": "ok"}
            for i in range(2)
        ]
        + [
            {"judge": f"j{i}", "generation_id": "gen_2", "match": None, "status": "ok"}
            for i in range(2, 5)
        ]
        + [
            {"judge": f"j{i}", "generation_id": "gen_3", "match": None, "status": "ok"}
            for i in range(5)
        ]
    )
    gold_ids = [f"g{i}" for i in range(1, 6)]
    agg = aggregate_model_topic(verdicts, gold_ids, [f"j{i}" for i in range(5)])

    g2_cells = agg["cells"][agg["cells"].gold_id == "g2"]
    weights = dict(zip(g2_cells.generation_id, g2_cells.weight, strict=False))
    assert weights == {"gen_1": 0.5, "gen_2": 0.2, "gen_3": 0.0}, weights
    gold = agg["gold"].set_index("gold_id")
    assert gold.loc["g2", "credit_sum"] == 0.7
    assert gold.loc["g2", "credit_max"] == 0.5
    assert gold.loc["g1", "credit_sum"] == 0.0
    # Credit-sum can never exceed 1: it is a share of judges by construction.
    assert (agg["gold"].credit_sum <= 1.0).all()
    assert agg["coverage_sum"] == 0.7 / 5
    assert agg["coverage_max"] == 0.5 / 5
    assert agg["n_generations"] == 3

    # Validity (precision input): raw share of ok judges assigning to any gold.
    validity = dict(zip(agg["validity"].generation_id, agg["validity"].validity, strict=False))
    assert validity["gen_1"] == 0.75  # 3 of the 4 non-errored judges matched
    assert validity["gen_2"] == 0.4  # 2 of 5
    assert validity["gen_3"] == 0.0

    # Family-disjoint panel resolution at analysis time.
    panels = {
        "families": {"gen_a": "a", "j0": "a", "j1": "b", "j2": "c", "j3": "d", "j4": "e",
                     "sub_z": "z"},
        "base_panel": ["j0", "j1", "j2", "j3", "j4"],
        "substitutions": {"a": "sub_z"},
    }
    resolved = resolve_panel("gen_a", panels, "disjoint")
    assert len(resolved) == 5 and "j0" not in resolved and "sub_z" in resolved

    # Agreement + multiple-comparison primitives used by stages 5 and 6.
    # Items are {category: rater_count}; two unanimous-but-differing items is
    # perfect agreement against a 50/50 chance baseline, so kappa == 1.
    assert fleiss_kappa([{"a": 5}, {"b": 5}]) == 1.0
    assert cohen_kappa(["a", "b", "a", "b"], ["a", "b", "a", "b"]) == 1.0
    # BH on a uniformly-spaced run collapses to the largest scaled value.
    assert all(abs(q - 0.03) < 1e-12 for q in bh_correction([0.01, 0.02, 0.03]))
    point, lo, hi = bootstrap_ci(pd.Series([1.0, 1.0, 1.0, 1.0]), n_boot=200, seed=0)
    assert point == lo == hi == 1.0  # zero-variance input has a degenerate CI

    # Parsing: fenced JSON, presented-label validation.
    text = 'noise\n```json\n[{"summary": "s", "explanation": "e"}]\n```'
    assert parse_perspectives(text)[0].summary == "s"
    judgment = parse_judgment('{"match": 3, "scope_ok": true, "reason": "r"}', n_gold=5)
    assert judgment.match == 3

    # Verify attributes coercion
    judgment_str_attr = parse_judgment(
        '{"match": 3, "scope_ok": true, "reason": "r", "attributes": "single stance details"}',
        n_gold=5
    )
    assert judgment_str_attr.attributes == ("single stance details",)

    judgment_list_attr = parse_judgment(
        '{"match": 3, "scope_ok": true, "reason": "r", "attributes": ["stance1", "stance2"]}',
        n_gold=5
    )
    assert judgment_list_attr.attributes == ("stance1", "stance2")

    try:
        parse_judgment(
            '{"match": 3, "scope_ok": true, "reason": "r", "attributes": 123}',
            n_gold=5
        )
        raise AssertionError("invalid attributes type must raise")
    except ParseError:
        pass

    try:
        parse_judgment('{"match": 6, "scope_ok": true, "reason": "r"}', n_gold=5)
        raise AssertionError("out-of-range match must raise")
    except ParseError:
        pass

    # .env loader: parses KEY=value, strips quotes, real env wins.
    with tempfile.TemporaryDirectory() as tmp:
        env_path = Path(tmp) / ".env"
        env_path.write_text(
            'OPENROUTER_API_KEY=from_file\n# comment\nFOO="bar"\n', encoding="utf-8"
        )
        os.environ.pop("OPENROUTER_API_KEY", None)
        os.environ["FOO"] = "real"
        _load_dotenv(env_path)
        assert os.environ["OPENROUTER_API_KEY"] == "from_file"
        assert os.environ["FOO"] == "real"  # existing var not overwritten
        os.environ.pop("OPENROUTER_API_KEY", None)

    print("test_smoke: all checks passed")


if __name__ == "__main__":
    main()
