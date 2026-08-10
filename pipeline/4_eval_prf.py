#!/usr/bin/env python3
"""
eval_prf.py — Step 5: Recall (coverage), Precision, and F1.

Per the Methodology:
  * Coverage per (model, topic) = mean gold credit over that topic's five
    golds; overall coverage = unweighted mean over the 16 topics.
  * Precision per (model, topic) = mean generation validity (raw share of
    judges assigning the generation to any gold); overall = mean over topics.
  * F1 = harmonic mean of overall coverage and overall precision; the model
    ranking is by F1, with coverage reported separately as the primary
    scientific quantity.
  * Confidence intervals: percentile bootstrap over topics (default 10,000
    resamples). The F1 CI resamples topics jointly for coverage and precision
    so their correlation is preserved.

--gold-credit sum|max selects the coverage rule (default: sum; see README).

Usage:
  python eval_prf.py --agg out/ --out out/ [--gold-credit sum] [--n-boot 10000]
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from bweird.analysis import bootstrap_ci, log

# Repo-root-relative defaults, resolved from this file so the stage runs from
# any working directory. Every path can still be overridden on the command line.
ROOT = Path(__file__).resolve().parent.parent
ADAPTED = ROOT / "results" / "adapted"
AGG = ROOT / "results" / "agg"


def harmonic(a, b):
    return 0.0 if (a + b) == 0 else 2 * a * b / (a + b)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--agg", default=str(AGG), help="directory with 3_aggregate.py outputs")
    ap.add_argument("--out", default=str(AGG))
    ap.add_argument("--gold-credit", choices=["sum", "max"], default="sum")
    ap.add_argument("--n-boot", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    agg = Path(args.agg)
    cov = pd.read_csv(agg / "coverage_topic.csv")
    prec = pd.read_csv(agg / "precision_topic.csv")
    ccol = f"coverage_{args.gold_credit}"

    df = cov.merge(prec, on=["generator", "topic_id"])
    n_topics = df.topic_id.nunique()
    incomplete = df.groupby("generator").topic_id.nunique()
    for g, k in incomplete.items():
        if k != n_topics:
            log.warning("generator %s has %d/%d topics", g, k, n_topics)

    rng = np.random.default_rng(args.seed)
    rows, per_topic = [], []
    for g, sub in df.groupby("generator"):
        sub = sub.sort_values("topic_id").reset_index(drop=True)
        c = sub[ccol].to_numpy(float)
        p = sub["precision"].to_numpy(float)
        cov_hat, cov_lo, cov_hi = bootstrap_ci(sub.set_index("topic_id")[ccol],
                                               n_boot=args.n_boot, seed=args.seed)
        prc_hat, prc_lo, prc_hi = bootstrap_ci(sub.set_index("topic_id")["precision"],
                                               n_boot=args.n_boot, seed=args.seed)
        # joint bootstrap for F1
        n = len(sub)
        idx = rng.integers(0, n, size=(args.n_boot, n))
        f1_boot = np.array([harmonic(c[i].mean(), p[i].mean()) for i in idx])
        f1_hat = harmonic(c.mean(), p.mean())
        f1_lo, f1_hi = np.percentile(f1_boot, [2.5, 97.5])
        rows.append((g, cov_hat, cov_lo, cov_hi, prc_hat, prc_lo, prc_hi,
                     f1_hat, float(f1_lo), float(f1_hi), n))
        per_topic.append(sub.assign(f1_topic=[harmonic(a, b) for a, b in zip(c, p, strict=False)]))

    ranking = pd.DataFrame(rows, columns=[
        "generator", "coverage", "coverage_lo", "coverage_hi",
        "precision", "precision_lo", "precision_hi",
        "f1", "f1_lo", "f1_hi", "n_topics",
    ]).sort_values("f1", ascending=False).reset_index(drop=True)

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    ranking.to_csv(out / "ranking.csv", index=False)
    pd.concat(per_topic, ignore_index=True).to_csv(out / "prf_per_topic.csv", index=False)

    disp = ranking.copy()
    for col in disp.columns[1:-1]:
        disp[col] = disp[col].round(3)
    print(f"\nModel ranking by F1 (coverage rule: {args.gold_credit}; "
          f"95% CIs from {args.n_boot} topic resamples):")
    print(disp.to_string(index=False))
    print(f"\nWritten: {out/'ranking.csv'}, {out/'prf_per_topic.csv'}")


if __name__ == "__main__":
    main()
