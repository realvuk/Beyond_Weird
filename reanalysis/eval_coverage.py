"""eval_coverage.py — canonical coverage / precision / F1 (rebuilds the lost script).

Coverage uses bw_common.panel_weights: per judge, credit for a matched gold is
split equally among however many generations that judge matched to it, then
averaged across judges. Matches the Methodology's existing "Aggregation"
paragraph exactly, and confirmed against results/agg/cells.csv and
gold_credit.csv to floating-point epsilon (NOT the one-to-one rule in
bw_common.one_to_one_assign, which is real code but isn't what produces
coverage — see that function's docstring). Produces Table 1 with 95%
bootstrap CIs (10,000 topic resamples) and a deviation report against
ranking.csv — a small deviation here is your confirmation the join, schema
mapping, and family-disjointness filter are all reading your real data
correctly.

Run:  python eval_coverage.py
      python eval_coverage.py --B 2000   # faster, wider CIs, for a quick check
"""
import argparse

import pandas as pd

import bw_common as bw


def fmt_row(r):
    return (f"{r['model']:<38s} "
            f"{r['coverage']:.4f} ({r['cov_lo']:.3f}-{r['cov_hi']:.3f})   "
            f"{r['precision']:.4f} ({r['prec_lo']:.3f}-{r['prec_hi']:.3f})   "
            f"{r['f1']:.4f} ({r['f1_lo']:.3f}-{r['f1_hi']:.3f})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--B", type=int, default=10_000, help="bootstrap resamples")
    args = ap.parse_args()

    data = bw.load_all()
    outdir = bw._outdir()

    summ = bw.bootstrap_model_summary(data["cov_mt"], data["prec_mt"], B=args.B)
    summ["published_as"] = summ["model"].map(lambda m: bw.published_label(m) or "")

    print("\n" + "=" * 100)
    print(f"TABLE 1  (B={args.B}, seed={bw.CONFIG['seed']})")
    print("=" * 100)
    print(f"{'model':<38s} {'coverage (95% CI)':<24s}  {'precision (95% CI)':<24s}  "
          f"{'F1 (95% CI)'}")
    for _, r in summ.iterrows():
        print(fmt_row(r))

    comp = []
    for _, r in summ.iterrows():
        lab = r["published_as"]
        pub = bw.PUBLISHED_TABLE1.get(lab)
        if pub:
            comp.append({"model": lab,
                         "d_cov": r["coverage"] - pub["coverage"],
                         "d_prec": r["precision"] - pub["precision"],
                         "d_f1": r["f1"] - pub["f1"]})
    unmatched = summ[summ["published_as"] == ""]["model"].tolist()
    if unmatched:
        print(f"\nWARNING: no published label found for {unmatched} — add to "
              f"_SLUG_TO_LABEL in bw_common.py so it's included in the check below.")
    if comp:
        c = pd.DataFrame(comp)
        print(f"\nmax |deviation| vs ranking.csv: cov {c['d_cov'].abs().max():.5f}  "
              f"prec {c['d_prec'].abs().max():.5f}  f1 {c['d_f1'].abs().max():.5f}")
        print("(should be ~0, i.e. matching to 4-5 decimal places; anything larger "
              "means something upstream — schema mapping, family filter, dedup — "
              "still disagrees with the real pipeline)")
        worst = c.reindex(c["d_f1"].abs().sort_values(ascending=False).index).head(3)
        print("\nlargest F1 deviations:")
        print(worst.to_string(index=False))

    p1 = outdir / "table1_model_summary.csv"
    summ.to_csv(p1, index=False)
    p2 = outdir / "coverage_model_topic.csv"
    data["cov_mt"].merge(data["prec_mt"], on=["generator", "topic"]).to_csv(p2, index=False)
    p3 = outdir / "per_gold_credit.csv"
    data["per_gold"].to_csv(p3, index=False)
    print(f"\nwrote {p1}\nwrote {p2}   (input for topic_difficulty.py / weird_gap.py)"
          f"\nwrote {p3}   (n = {len(data['per_gold'])}; expect 13*16*5 = 1,040 rows"
          f" — one per (model, topic, gold_slot), credit already 0 for unassigned golds)")


if __name__ == "__main__":
    main()
