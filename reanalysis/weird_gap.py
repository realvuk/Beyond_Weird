"""weird_gap.py — the primary WEIRD-gap test and its robustness checks.

Recomputes: pooled exact Wilcoxon over the eight matched-pair deltas (one- and
two-sided), rank-biserial effect size, 10k bootstrap CI over pairs, the
per-model Wilcoxon table with BH correction, and the precision-side (junk-rate)
paired test. Compares against the published numbers so any divergence from the
rule/join surfaces immediately. Shared by lojo_audit.py.

Run:  python weird_gap.py
"""
import numpy as np
import pandas as pd

import bw_common as bw


def pooled_test(deltas_by_pair, label="coverage"):
    d = np.asarray(deltas_by_pair, float)
    w1, p1, n1, _ = bw.exact_wilcoxon(d, alternative="greater")
    w2, p2, n2, r = bw.exact_wilcoxon(d, alternative="two-sided")
    rng = np.random.default_rng(bw.CONFIG["seed"])
    boots = np.mean(d[rng.integers(0, len(d), size=(10_000, len(d)))], axis=1)
    lo, hi = np.percentile(boots, [2.5, 97.5])
    print(f"pooled {label} gap: mean {np.mean(d):+.3f}  median {np.median(d):+.3f}  "
          f"95% CI [{lo:+.3f}, {hi:+.3f}]")
    print(f"  one-sided (WEIRD>Serbian) p = {p1:.2f}   two-sided p = {p2:.2f}   "
          f"rank-biserial r = {r:+.2f}   (n_eff = {n2})")
    return {"mean": float(np.mean(d)), "median": float(np.median(d)),
            "ci": (float(lo), float(hi)), "p1": p1, "p2": p2, "r": r}


def main():
    data = bw.load_all()
    gold, cov_mt, prec_mt = data["gold"], data["cov_mt"], data["prec_mt"]
    outdir = bw._outdir()

    piv = bw.pair_deltas(cov_mt, gold)  # per (model, pair): delta = W - S

    print("\n" + "=" * 78)
    print("PRIMARY TEST — pooled over models, unit = matched pair (n = 8)")
    print("=" * 78)
    pair_means = piv.groupby("pair")["delta"].mean().sort_index()
    print("per-pair deltas (mean over models):")
    for pair, v in pair_means.items():
        print(f"  {pair}: {v:+.3f}")
    pooled_test(pair_means.values, "coverage")
    pub = bw.PUBLISHED_GAP
    print(f"published: mean {pub['pooled_mean']:+.3f}  median "
          f"{pub['pooled_median']:+.3f}  CI [{pub['ci'][0]:+.3f}, "
          f"{pub['ci'][1]:+.3f}]  p1 {pub['p_one_sided']}  p2 {pub['p_two_sided']}  "
          f"r {pub['rank_biserial']:+.2f}")

    print("\n" + "=" * 78)
    print("PER-MODEL GAPS (exact Wilcoxon over 8 pairs, BH-adjusted)")
    print("=" * 78)
    rows = []
    for model, grp in piv.groupby("generator"):
        d = grp.sort_values("pair")["delta"].to_numpy()
        _, p1, _, _ = bw.exact_wilcoxon(d, alternative="greater")
        rows.append({"model": bw.published_label(model) or str(model),
                     "mean_gap": np.mean(d), "median_gap": np.median(d),
                     "p_one_sided": p1})
    pm = pd.DataFrame(rows).sort_values("mean_gap", ascending=False)
    pm["p_BH"] = bw.bh_adjust(pm["p_one_sided"].values)
    with pd.option_context("display.float_format", "{:+.3f}".format):
        print(pm.to_string(index=False,
                           formatters={"p_one_sided": "{:.3f}".format,
                                       "p_BH": "{:.3f}".format}))

    print("\n" + "=" * 78)
    print("PRECISION-SIDE CHECK (junk rate = 1 - precision, paired over arms)")
    print("=" * 78)
    jr = prec_mt.copy()
    jr["junk"] = 1 - jr["precision"]
    meta = gold[["topic", "pair", "arm"]].dropna()
    meta["topic"] = meta["topic"].astype(str)
    j = jr.merge(meta, on="topic")
    jp = (j.pivot_table(index=["generator", "pair"], columns="arm",
                        values="junk", aggfunc="mean").reset_index())
    jp["delta"] = jp["WEIRD"] - jp["SERBIAN"]
    jpair = jp.groupby("pair")["delta"].mean()
    pooled_test(jpair.values, "junk-rate")
    print("published: median +0.035  mean +0.017  CI [-0.050, +0.075]  "
          "two-sided p = 0.55")

    piv.to_csv(outdir / "pair_deltas_model.csv", index=False)
    pair_means.rename("delta").to_csv(outdir / "pair_deltas_pooled.csv")
    pm.to_csv(outdir / "per_model_gap.csv", index=False)
    print(f"\nwrote {outdir}/pair_deltas_model.csv, pair_deltas_pooled.csv, "
          f"per_model_gap.csv")


if __name__ == "__main__":
    main()
