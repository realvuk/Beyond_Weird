"""lojo_audit.py — leave-one-judge-out sensitivity audit (step 10).

Without human labels, LOJO no longer tests 'does the panel beat its best
member'; it tests whether any single judge DRIVES the results. For each judge
model (base panel and substitutes), all of that judge's verdicts are removed,
weights are recomputed over the remaining judges, and we report:

  - Spearman rho between the full-panel and reduced-panel model rankings
    (coverage and F1), and whether the top model changes;
  - the pooled WEIRD-gap mean and two-sided p under the exclusion;
  - the largest per-model coverage shift.

The Gemini judge is the pre-registered focus (most distinctive rater).

Run:  python lojo_audit.py
"""
import numpy as np
import pandas as pd
from scipy import stats

import bw_common as bw


def summarise(valid, gold):
    gen_tab = bw.generation_table(valid)
    cov_mt, prec_mt, _ = bw.model_topic_tables(valid, gen_tab)
    cov = cov_mt.groupby("generator")["coverage"].mean()
    prec = prec_mt.groupby("generator")["precision"].mean()
    f1 = 2 * cov * prec / (cov + prec)
    piv = bw.pair_deltas(cov_mt, gold)
    pair_means = piv.groupby("pair")["delta"].mean().values
    _, p2, _, _ = bw.exact_wilcoxon(pair_means, alternative="two-sided")
    return cov, f1, float(np.mean(pair_means)), p2


def main():
    data = bw.load_all()
    valid, gold = data["valid"], data["gold"]

    full_cov, full_f1, full_gap, full_p = summarise(valid, gold)
    order = full_cov.sort_values(ascending=False)
    print(f"\nFULL PANEL: top model {bw.published_label(order.index[0]) or order.index[0]} "
          f"({order.iloc[0]:.3f}); pooled gap {full_gap:+.3f}, two-sided p {full_p:.2f}")

    judges = sorted(valid["judge"].astype(str).unique())
    print(f"judges found ({len(judges)}): {judges}\n")

    rows = []
    for j in judges:
        sub = valid[valid["judge"].astype(str) != j]
        n_dropped = len(valid) - len(sub)
        cov, f1, gap, p2 = summarise(sub, gold)

        common = full_cov.index.intersection(cov.index)
        rho_c = stats.spearmanr(full_cov[common], cov[common]).statistic
        rho_f = stats.spearmanr(full_f1[common], f1[common]).statistic
        top = cov.sort_values(ascending=False).index[0]
        shift = (cov[common] - full_cov[common])
        worst = shift.abs().idxmax()

        rows.append({
            "judge_removed": j,
            "verdicts_removed": n_dropped,
            "rho_coverage": rho_c,
            "rho_f1": rho_f,
            "top_model_same": top == order.index[0],
            "pooled_gap": gap,
            "p_two_sided": p2,
            "max_model_shift": shift[worst],
            "shifted_model": bw.published_label(worst) or str(worst),
        })

    df = pd.DataFrame(rows)
    with pd.option_context("display.width", 160, "display.max_columns", 20,
                           "display.float_format", "{:+.3f}".format):
        print(df.to_string(index=False,
                           formatters={"p_two_sided": "{:.2f}".format,
                                       "verdicts_removed": "{:d}".format}))

    print("\nREADING: the panel is robust if every rho >= ~0.9, the top model never "
          "changes, and the two-sided p never approaches 0.05. Report the Gemini-judge "
          "row explicitly in 4.5 (it is the most distinctive rater); a stable null "
          "under its exclusion closes the 'one idiosyncratic judge drives the result' "
          "objection that the dropped per-judge human audit used to address.")

    out = bw._outdir() / "lojo_audit.csv"
    df.to_csv(out, index=False)
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
