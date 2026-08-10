#!/usr/bin/env python3
"""
eval_stats.py — Step 8: ranking statistics and the matched-pairs WEIRD-gap
analysis.

Per the Methodology:
  * Pairwise model comparisons: paired sign-flip permutation tests on
    per-topic coverage differences (10,000 iterations), Benjamini-Hochberg
    adjusted. Interpreted at tier level given 16 topics.
  * PRIMARY: WEIRD gap. Unit = matched topic pair. For each of the 8 pairs,
    delta = coverage(WEIRD arm) - coverage(Serbian arm), averaged across
    models -> 8 paired values, tested against zero with an exact Wilcoxon
    signed-rank test. The hypothesised direction (WEIRD > Serbian) is fixed
    in advance, so the one-sided test is primary; the two-sided p is
    reported alongside, with the median paired gap, the matched-pairs
    rank-biserial effect size, and a bootstrap CI over pairs. A null result
    is informative and reported as such.
  * SECONDARY: the same Wilcoxon per model (BH-adjusted) to identify which
    models carry the gap; a mixed-effects robustness check on per-gold
    credit with crossed random effects for topic pair and generator
    (statsmodels MixedLM via variance components); and the identical paired
    test on the junk rate (1 - precision) for precision-side asymmetries.

Usage:
  python eval_stats.py --agg out/ --topics topics.json --out out/ \
      [--gold-credit sum] [--n-perm 10000] [--n-boot 10000]
"""
import argparse
import math
import warnings
from functools import partial
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import rankdata, wilcoxon

from bweird.analysis import bh_correction, load_topics, log

# ------------------------------------------------------------------ helpers

# Repo-root-relative defaults, resolved from this file so the stage runs from
# any working directory. Every path can still be overridden on the command line.
ROOT = Path(__file__).resolve().parent.parent
ADAPTED = ROOT / "results" / "adapted"
AGG = ROOT / "results" / "agg"


def exact_wilcoxon(d, alternative):
    d = np.asarray(d, float)
    nz = d[d != 0]
    if len(nz) == 0:
        return float("nan")
    try:
        return float(wilcoxon(nz, alternative=alternative, method="exact").pvalue)
    except (TypeError, ValueError):        # older scipy or ties fallback
        return float(wilcoxon(nz, alternative=alternative).pvalue)


def rank_biserial(d):
    """Matched-pairs rank-biserial correlation: (W+ - W-)/(W+ + W-)."""
    d = np.asarray(d, float)
    d = d[d != 0]
    if len(d) == 0:
        return float("nan")
    r = rankdata(np.abs(d))
    w_pos = r[d > 0].sum()
    return float((2 * w_pos - r.sum()) / r.sum())


def paired_permutation(x, y, n_iter, rng):
    """Two-sided sign-flip permutation test on paired mean difference."""
    d = np.asarray(x, float) - np.asarray(y, float)
    obs = d.mean()
    signs = rng.choice([-1.0, 1.0], size=(n_iter, len(d)))
    null = (signs * d).mean(axis=1)
    p = (np.sum(np.abs(null) >= abs(obs) - 1e-12) + 1) / (n_iter + 1)
    return float(obs), float(p)


def pair_deltas(per_topic, topics, value_col):
    """Wide per-(generator, pair) deltas: value(weird arm) - value(serbian arm)."""
    t = per_topic.copy()
    t["pair_id"] = t.topic_id.map(lambda x: topics[x]["pair_id"])
    t["arm"] = t.topic_id.map(lambda x: topics[x]["arm"])
    wide = t.pivot_table(index=["generator", "pair_id"], columns="arm",
                         values=value_col, aggfunc="mean").reset_index()
    if not {"weird", "serbian"} <= set(wide.columns):
        raise ValueError("need both arms present to compute pair deltas")
    wide["delta"] = wide["weird"] - wide["serbian"]
    return wide.dropna(subset=["delta"])


def gap_test(deltas_by_pair, n_boot, rng, label):
    d = deltas_by_pair.to_numpy(float)
    res = {
        "analysis": label,
        "n_pairs": len(d),
        "mean_gap": float(d.mean()),
        "median_gap": float(np.median(d)),
        "p_one_sided_weird_gt": exact_wilcoxon(d, "greater"),
        "p_two_sided": exact_wilcoxon(d, "two-sided"),
        "rank_biserial": rank_biserial(d),
    }
    idx = rng.integers(0, len(d), size=(n_boot, len(d)))
    boots = d[idx]
    res["mean_ci_lo"], res["mean_ci_hi"] = map(float, np.percentile(boots.mean(1), [2.5, 97.5]))
    res["median_ci_lo"], res["median_ci_hi"] = map(
        float, np.percentile(np.median(boots, 1), [2.5, 97.5]))
    return res



def _sig(x, digits):
    """Round to `digits` significant figures, passing NaN/inf through."""
    x = float(x)
    if not math.isfinite(x) or x == 0.0:
        return x
    return round(x, digits - 1 - math.floor(math.log10(abs(x))))


def mixed_model(gold_credit, topics, credit_col):
    try:
        import statsmodels.formula.api as smf
    except ImportError:
        log.warning("statsmodels not installed; mixed-effects check skipped")
        return None
    df = gold_credit.copy()
    df["pair_id"] = df.topic_id.map(lambda x: topics[x]["pair_id"])
    df["arm"] = pd.Categorical(df.topic_id.map(lambda x: topics[x]["arm"]),
                               categories=["serbian", "weird"])
    df["credit"] = df[credit_col]
    df["one_group"] = 1  # crossed random effects via variance components
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        model = smf.mixedlm(
            "credit ~ C(arm)", data=df, groups="one_group",
            vc_formula={"pair": "0 + C(pair_id)", "generator": "0 + C(generator)"})
        fit = model.fit(reml=True, method="lbfgs")
    coef = fit.params.get("C(arm)[T.weird]", float("nan"))
    se = fit.bse.get("C(arm)[T.weird]", float("nan"))
    p = fit.pvalues.get("C(arm)[T.weird]", float("nan"))
    # Round to 12 significant digits. L-BFGS converges to a tolerance, not to
    # the last bit, so the raw values wobble around the 1e-16 mark between
    # statsmodels/SciPy builds. Everything else in results/ is exact, and 12
    # digits is far beyond anything reported; this keeps the committed CSV
    # bit-for-bit reproducible instead of dirtying the tree on every re-run.
    r12 = partial(_sig, digits=12)
    return {"arm_weird_coef": r12(coef), "se": r12(se), "p": r12(p),
            "n_obs": int(fit.nobs)}


# --------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--agg", default=str(AGG), help="directory with 3_aggregate.py outputs")
    ap.add_argument("--topics", default=str(ADAPTED / "topics.json"))
    ap.add_argument("--out", default=str(AGG))
    ap.add_argument("--gold-credit", choices=["sum", "max"], default="sum")
    ap.add_argument("--n-perm", type=int, default=10000)
    ap.add_argument("--n-boot", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    rng = np.random.default_rng(args.seed)
    topics = load_topics(args.topics)
    agg = Path(args.agg)
    cov = pd.read_csv(agg / "coverage_topic.csv")
    prec = pd.read_csv(agg / "precision_topic.csv")
    gold_credit = pd.read_csv(agg / "gold_credit.csv")
    ccol = f"coverage_{args.gold_credit}"
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    # ---- pairwise model comparisons -------------------------------------
    print("\n=== Pairwise model comparisons (paired permutation on per-topic "
          "coverage; BH-adjusted) ===")
    piv = cov.pivot_table(index="topic_id", columns="generator", values=ccol)
    models = sorted(piv.columns)
    rows = []
    for a, b in combinations(models, 2):
        both = piv[[a, b]].dropna()
        diff, p = paired_permutation(both[a], both[b], args.n_perm, rng)
        rows.append((a, b, diff, p))
    pw = pd.DataFrame(rows, columns=["model_a", "model_b",
                                     "mean_coverage_diff", "p_raw"])
    pw["p_bh"] = bh_correction(pw.p_raw.tolist())
    pw = pw.sort_values("p_bh").reset_index(drop=True)
    pw.to_csv(out / "pairwise_models.csv", index=False)
    n_nom = int((pw.p_raw < 0.05).sum())
    n_bh = int((pw.p_bh < 0.05).sum())
    print(f"  {len(pw)} pairs: {n_nom} nominally significant, "
          f"{n_bh} survive BH at alpha=0.05")
    print(pw.head(8).round(4).to_string(index=False))

    # ---- primary WEIRD gap ----------------------------------------------
    print("\n=== PRIMARY: WEIRD gap (pooled over models; unit = matched pair; "
          "exact Wilcoxon) ===")
    deltas = pair_deltas(cov, topics, ccol)
    pooled = deltas.groupby("pair_id").delta.mean()
    primary = gap_test(pooled, args.n_boot, rng, "pooled_coverage")
    for k, v in primary.items():
        print(f"  {k:24s} {v:.4f}" if isinstance(v, float) else f"  {k:24s} {v}")
    pooled.rename("mean_delta").reset_index().to_csv(
        out / "weird_gap_pair_deltas.csv", index=False)

    # ---- secondary: per-model gaps --------------------------------------
    print("\n=== Secondary: per-model WEIRD gap (exact Wilcoxon over 8 pairs; "
          "BH-adjusted) ===")
    pm_rows = []
    for g, sub in deltas.groupby("generator"):
        d = sub.delta.to_numpy(float)
        pm_rows.append((g, len(d), float(d.mean()), float(np.median(d)),
                        exact_wilcoxon(d, "greater"), rank_biserial(d)))
    pm = pd.DataFrame(pm_rows, columns=["generator", "n_pairs", "mean_gap",
                                        "median_gap", "p_one_sided",
                                        "rank_biserial"])
    pm["p_bh"] = bh_correction(pm.p_one_sided.tolist())
    pm = pm.sort_values("mean_gap", ascending=False).reset_index(drop=True)
    pm.to_csv(out / "weird_gap_per_model.csv", index=False)
    print(pm.round(4).to_string(index=False))

    # ---- secondary: mixed-effects robustness check ----------------------
    print("\n=== Secondary: mixed-effects robustness check "
          "(per-gold credit ~ arm, random: pair + generator) ===")
    mm = mixed_model(gold_credit, topics, f"credit_{args.gold_credit}")
    if mm:
        print(f"  arm[weird] coefficient = {mm['arm_weird_coef']:+.4f} "
              f"(SE {mm['se']:.4f}, p = {mm['p']:.4f}, n = {mm['n_obs']})")
        pd.DataFrame([mm]).to_csv(out / "mixed_model.csv", index=False)

    # ---- secondary: precision-side gap (junk rate) ----------------------
    print("\n=== Secondary: precision-side gap (junk rate = 1 - precision; "
          "pooled exact Wilcoxon) ===")
    junk = prec.assign(junk=lambda d: 1 - d.precision)
    jdeltas = pair_deltas(junk, topics, "junk").groupby("pair_id").delta.mean()
    jres = gap_test(jdeltas, args.n_boot, rng, "pooled_junk_rate")
    for k, v in jres.items():
        print(f"  {k:24s} {v:.4f}" if isinstance(v, float) else f"  {k:24s} {v}")

    pd.DataFrame([primary, jres]).to_csv(out / "weird_gap_summary.csv", index=False)
    print(f"\nArtifacts written to {out}/")


if __name__ == "__main__":
    main()
