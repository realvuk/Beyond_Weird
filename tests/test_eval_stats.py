"""Focused tests for the statistical procedures in pipeline/6_eval_stats.py."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

SPEC = importlib.util.spec_from_file_location(
    "eval_stats", Path(__file__).parents[1] / "pipeline" / "6_eval_stats.py"
)
assert SPEC and SPEC.loader
EVAL_STATS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EVAL_STATS)


def test_exact_signed_rank_drops_zeros_and_uses_tied_midranks():
    # Nonzero absolute differences are all tied, so each has midrank 2.
    # Observed W+ is 4; four of the eight sign assignments have W+ >= 4.
    exact_signed_rank = getattr(EVAL_STATS, "exact_signed_rank", lambda _d: (None, None))
    p, effect = exact_signed_rank([1.0, 1.0, -1.0, 0.0])

    assert p == pytest.approx(0.5)
    assert effect == pytest.approx(1 / 3)


def test_exact_signed_rank_recovers_exact_ties_from_float_arithmetic():
    # These are exactly {+0.3, +0.3, -0.3, 0} before binary-float noise.
    p, effect = EVAL_STATS.exact_signed_rank([0.1 + 0.2, 0.3, -0.3, 1e-17])

    assert p == pytest.approx(0.5)
    assert effect == pytest.approx(1 / 3)


def test_t_summary_reproduces_reported_primary_interval_and_mde():
    # The eight pair-level WEIRD-minus-Serbian gaps reported in Appendix D.2.
    d = [0.000769, 0.055385, 0.003077, -0.028846, -0.169231, 0.190769, -0.100769, -0.055769]
    r = EVAL_STATS.t_summary(d)

    assert (r["mean_t_lo"], r["mean_t_hi"]) == pytest.approx((-0.1029, 0.0768), abs=1e-4)
    assert r["mean_upper_one_sided"] == pytest.approx(0.0589, abs=1e-4)
    assert r["power_at_gap_0.05"] == pytest.approx(0.324, abs=1e-3)
    assert r["mde_80pct"] == pytest.approx(0.1051, abs=1e-4)
