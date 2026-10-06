"""Regression pins for bweird.analysis: the aggregation and stats core.

Every number in results/agg/ comes from this module. These tests pin its
current, published behavior so refactors (dedup, library swaps) can be
checked against a known-good baseline rather than "it still runs".
"""
from __future__ import annotations

import json
from collections import Counter

import numpy as np
import pandas as pd
import pytest

from bweird import analysis as A
from bweird.errors import BweirdError

# ---------------------------------------------------------------------------
# File loaders: load_topics (eval-contract shape), load_panels, load_verdicts
# ---------------------------------------------------------------------------

EVAL_TOPICS_JSON = {
    "topics": [
        {"topic_id": "kosovo", "pair_id": "secession", "arm": "serbian",
         "gold_ids": ["kos_p1", "kos_p2", "kos_p3", "kos_p4", "kos_p5"]},
        {"topic_id": "quebec", "pair_id": "secession", "arm": "weird",
         "gold_ids": ["que_p1", "que_p2", "que_p3", "que_p4", "que_p5"]},
    ]
}


def test_load_eval_topics_valid(tmp_path):
    path = tmp_path / "topics.json"
    path.write_text(json.dumps(EVAL_TOPICS_JSON), encoding="utf-8")
    topics = A.load_eval_topics(path)
    assert set(topics) == {"kosovo", "quebec"}
    assert topics["kosovo"]["arm"] == "serbian"


def test_load_eval_topics_duplicate_id_raises(tmp_path):
    dup = {"topics": EVAL_TOPICS_JSON["topics"] + [EVAL_TOPICS_JSON["topics"][0]]}
    path = tmp_path / "topics.json"
    path.write_text(json.dumps(dup), encoding="utf-8")
    with pytest.raises(BweirdError):
        A.load_eval_topics(path)


def test_load_eval_topics_invalid_arm_raises(tmp_path):
    bad = {"topics": [{"topic_id": "x", "pair_id": "p", "arm": "martian",
                       "gold_ids": ["a"]}]}
    path = tmp_path / "topics.json"
    path.write_text(json.dumps(bad), encoding="utf-8")
    with pytest.raises(BweirdError):
        A.load_eval_topics(path)


def test_load_panels_valid(tmp_path):
    panels = {"families": {"j0": "a"}, "base_panel": ["j0"], "substitutions": {}}
    path = tmp_path / "panels.json"
    path.write_text(json.dumps(panels), encoding="utf-8")
    loaded = A.load_panels(path)
    assert loaded == panels


def test_load_panels_missing_key_raises(tmp_path):
    path = tmp_path / "panels.json"
    path.write_text(json.dumps({"families": {}}), encoding="utf-8")
    with pytest.raises(BweirdError):
        A.load_panels(path)


def test_load_panels_base_judge_missing_family_raises(tmp_path):
    panels = {"families": {}, "base_panel": ["j0"], "substitutions": {}}
    path = tmp_path / "panels.json"
    path.write_text(json.dumps(panels), encoding="utf-8")
    with pytest.raises(BweirdError):
        A.load_panels(path)


def test_load_verdicts_valid(tmp_path):
    topics = {"kosovo": {"gold_ids": ["kos_p1", "kos_p2"]}}
    rows = [
        {"generator": "g", "topic_id": "kosovo", "generation_id": "gen_1",
         "judge": "j0", "match": "kos_p1", "status": "ok"},
    ]
    path = tmp_path / "verdicts.jsonl"
    path.write_text("\n".join(json.dumps(r) for r in rows), encoding="utf-8")
    df = A.load_verdicts(path, topics)
    assert len(df) == 1
    assert df.iloc[0]["match"] == "kos_p1"


def test_load_verdicts_unknown_gold_id_demoted_to_no_match(tmp_path):
    topics = {"kosovo": {"gold_ids": ["kos_p1"]}}
    rows = [
        {"generator": "g", "topic_id": "kosovo", "generation_id": "gen_1",
         "judge": "j0", "match": "not_a_real_gold", "status": "ok"},
    ]
    path = tmp_path / "verdicts.jsonl"
    path.write_text("\n".join(json.dumps(r) for r in rows), encoding="utf-8")
    df = A.load_verdicts(path, topics)
    assert pd.isna(df.iloc[0]["match"])


def test_load_verdicts_duplicate_keeps_last(tmp_path):
    topics = {"kosovo": {"gold_ids": ["kos_p1", "kos_p2"]}}
    rows = [
        {"generator": "g", "topic_id": "kosovo", "generation_id": "gen_1",
         "judge": "j0", "match": "kos_p1", "status": "ok"},
        {"generator": "g", "topic_id": "kosovo", "generation_id": "gen_1",
         "judge": "j0", "match": "kos_p2", "status": "ok"},
    ]
    path = tmp_path / "verdicts.jsonl"
    path.write_text("\n".join(json.dumps(r) for r in rows), encoding="utf-8")
    df = A.load_verdicts(path, topics)
    assert len(df) == 1
    assert df.iloc[0]["match"] == "kos_p2"


def test_load_verdicts_unknown_topic_raises(tmp_path):
    path = tmp_path / "verdicts.jsonl"
    path.write_text(json.dumps({"generator": "g", "topic_id": "nope",
                                "generation_id": "gen_1", "judge": "j0",
                                "match": None, "status": "ok"}), encoding="utf-8")
    with pytest.raises(BweirdError):
        A.load_verdicts(path, {"kosovo": {"gold_ids": []}})


def test_load_verdicts_empty_raises(tmp_path):
    path = tmp_path / "verdicts.jsonl"
    path.write_text("", encoding="utf-8")
    with pytest.raises(BweirdError):
        A.load_verdicts(path, {})

# ---------------------------------------------------------------------------
# aggregate_model_topic — hand-derived worked example (see verify/test_smoke.py
# for the derivation in prose; duplicated here as the pytest regression pin).
# ---------------------------------------------------------------------------

def _worked_example_verdicts() -> pd.DataFrame:
    return pd.DataFrame(
        [{"judge": f"j{i}", "generation_id": "gen_1", "match": "g2", "status": "ok"}
         for i in range(3)]
        + [{"judge": "j3", "generation_id": "gen_1", "match": None, "status": "ok"},
           {"judge": "j4", "generation_id": "gen_1", "match": None, "status": "error"}]
        + [{"judge": f"j{i}", "generation_id": "gen_2", "match": "g2", "status": "ok"}
           for i in range(2)]
        + [{"judge": f"j{i}", "generation_id": "gen_2", "match": None, "status": "ok"}
           for i in range(2, 5)]
        + [{"judge": f"j{i}", "generation_id": "gen_3", "match": None, "status": "ok"}
           for i in range(5)]
    )


def test_aggregate_model_topic_worked_example():
    gold_ids = [f"g{i}" for i in range(1, 6)]
    agg = A.aggregate_model_topic(
        _worked_example_verdicts(), gold_ids, [f"j{i}" for i in range(5)]
    )

    g2 = agg["cells"][agg["cells"].gold_id == "g2"]
    weights = dict(zip(g2.generation_id, g2.weight, strict=False))
    assert weights == {"gen_1": 0.5, "gen_2": 0.2, "gen_3": 0.0}

    gold = agg["gold"].set_index("gold_id")
    assert gold.loc["g2", "credit_sum"] == 0.7
    assert gold.loc["g2", "credit_max"] == 0.5
    assert gold.loc["g1", "credit_sum"] == 0.0
    assert (agg["gold"].credit_sum <= 1.0).all()
    assert agg["coverage_sum"] == pytest.approx(0.7 / 5)
    assert agg["coverage_max"] == pytest.approx(0.5 / 5)
    assert agg["n_generations"] == 3

    validity = dict(zip(agg["validity"].generation_id, agg["validity"].validity, strict=False))
    assert validity["gen_1"] == 0.75
    assert validity["gen_2"] == 0.4
    assert validity["gen_3"] == 0.0


def test_aggregate_model_topic_raises_on_no_generations():
    empty = pd.DataFrame(columns=["judge", "generation_id", "match", "status"])
    with pytest.raises(ValueError):
        A.aggregate_model_topic(empty, ["g1"], ["j0"])


# ---------------------------------------------------------------------------
# Panel resolution
# ---------------------------------------------------------------------------

PANELS = {
    "families": {
        "gen_a": "a", "gen_x": "x", "j0": "a", "j1": "b", "j2": "c", "j3": "d",
        "j4": "e", "sub_z": "z",
    },
    "base_panel": ["j0", "j1", "j2", "j3", "j4"],
    "substitutions": {"a": "sub_z"},
}


def test_resolve_panel_substitutes_same_family_judge():
    resolved = A.resolve_panel("gen_a", PANELS, "disjoint")
    assert len(resolved) == 5
    assert "j0" not in resolved
    assert "sub_z" in resolved


def test_resolve_panel_no_substitution_needed():
    # gen_x's family ("x") isn't on the base panel, so no substitution triggers.
    resolved = A.resolve_panel("gen_x", PANELS, "disjoint")
    assert sorted(resolved) == sorted(PANELS["base_panel"])


def test_resolve_panel_full_mode_returns_base_panel():
    resolved = A.resolve_panel("gen_a", PANELS, "full")
    assert sorted(resolved) == sorted(PANELS["base_panel"])


def test_resolve_panel_missing_generator_family_raises():
    with pytest.raises(BweirdError):
        A.resolve_panel("unknown_generator", PANELS, "disjoint")


def test_resolve_panel_missing_substitute_raises():
    bad_panels = {**PANELS, "substitutions": {}}
    with pytest.raises(BweirdError):
        A.resolve_panel("gen_a", bad_panels, "disjoint")


# ---------------------------------------------------------------------------
# Agreement metrics — golden values captured from the current implementation
# on a fixed synthetic fixture (mixed unanimous / split / variable-rater
# items), cross-checked against verify/reverify.py's independent rel_coeffs()
# at swap time.
# ---------------------------------------------------------------------------

AGREEMENT_ITEMS = [
    Counter({"0": 3, "1": 2}),
    Counter({"1": 5}),
    Counter({"0": 5}),
    Counter({"2": 2, "0": 1, "1": 2}),
    Counter({"3": 4, "0": 1}),
]


def test_fleiss_kappa_golden_value():
    assert A.fleiss_kappa(AGREEMENT_ITEMS) == pytest.approx(0.46933962264150947, abs=1e-9)


def test_gwet_ac1_golden_value():
    assert A.gwet_ac1(AGREEMENT_ITEMS) == pytest.approx(0.534803583735355, abs=1e-9)


def test_krippendorff_alpha_golden_value():
    assert A.krippendorff_alpha(AGREEMENT_ITEMS) == pytest.approx(0.49056603773584906, abs=1e-9)


def test_fleiss_kappa_perfect_agreement_is_one():
    assert A.fleiss_kappa([{"a": 5}, {"b": 5}]) == 1.0


def test_cohen_kappa_perfect_agreement_is_one():
    assert A.cohen_kappa(["a", "b", "a", "b"], ["a", "b", "a", "b"]) == 1.0


def test_cohen_kappa_golden_value():
    a = ["x", "y", "x", "y", "x", "x"]
    b = ["x", "y", "y", "y", "x", "x"]
    assert A.cohen_kappa(a, b) == pytest.approx(0.6666666666666667, abs=1e-9)


def test_cohen_kappa_disjoint_categories_between_raters():
    # rater `a` never uses category "z"; rater `b` never uses "w" -- exercises
    # the union-of-categories path.
    a = ["w", "x", "x", "y"]
    b = ["z", "x", "x", "y"]
    kappa = A.cohen_kappa(a, b)
    assert -1.0 <= kappa <= 1.0


def test_cohen_kappa_empty_is_nan():
    assert np.isnan(A.cohen_kappa([], []))


# ---------------------------------------------------------------------------
# Benjamini-Hochberg correction
# ---------------------------------------------------------------------------

def test_bh_correction_golden_values():
    pvals = [0.001, 0.2, 0.03, 0.5, 0.049, 0.0001, 0.9, 0.15]
    got = A.bh_correction(pvals)
    expected = [
        0.004, 0.26666666666666666, 0.08, 0.5714285714285714,
        0.098, 0.0008, 0.9, 0.24,
    ]
    assert got == pytest.approx(expected, abs=1e-9)


def test_bh_correction_uniform_run_collapses_to_max():
    q = A.bh_correction([0.01, 0.02, 0.03])
    assert all(abs(x - 0.03) < 1e-12 for x in q)


def test_bh_correction_empty():
    assert A.bh_correction([]) == []


# ---------------------------------------------------------------------------
# Bootstrap CI — deterministic given a fixed seed; not swapped for a library
# implementation (a different sampling scheme would move published CIs), so
# this pins its current output rather than the algorithm's correctness.
# ---------------------------------------------------------------------------

def test_bootstrap_ci_degenerate_input():
    point, lo, hi = A.bootstrap_ci(pd.Series([1.0, 1.0, 1.0, 1.0]), n_boot=200, seed=0)
    assert point == lo == hi == 1.0


def test_bootstrap_ci_deterministic_for_fixed_seed():
    vals = pd.Series([0.1, 0.4, 0.6, 0.9, 0.3])
    a = A.bootstrap_ci(vals, n_boot=500, seed=42)
    b = A.bootstrap_ci(vals, n_boot=500, seed=42)
    assert a == b


def test_bootstrap_ci_empty_series():
    point, lo, hi = A.bootstrap_ci(pd.Series([], dtype=float), n_boot=10, seed=0)
    assert np.isnan(point) and np.isnan(lo) and np.isnan(hi)


# ---------------------------------------------------------------------------
# plurality_verdict
# ---------------------------------------------------------------------------

def test_plurality_verdict_majority():
    verdict, share = A.plurality_verdict(["g1", "g1", "g1", None, "g2"])
    assert verdict == "g1"
    assert share == pytest.approx(3 / 5)


def test_plurality_verdict_tie_breaks_toward_no_match():
    verdict, _ = A.plurality_verdict(["g1", "g1", None, None])
    assert verdict == A.NO_MATCH


def test_plurality_verdict_tie_among_golds_breaks_lexicographically():
    verdict, _ = A.plurality_verdict(["g2", "g1"])
    assert verdict == "g1"
