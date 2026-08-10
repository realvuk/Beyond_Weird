#!/usr/bin/env python3
"""
aggregate.py — Step 4 of the workflow: aggregate judge votes into continuous,
soft agreement weights via the split-then-average matrix scheme.

For each (generator, topic) it builds one matrix per judge (rows = generated
perspectives, columns = gold perspectives), applies the within-judge split
rule (k generations matched to the same gold share one unit of credit, 1/k
each), averages cell-wise across the panel with per-generation denominators
(abstaining/erroring judges are dropped from the affected cells only), and
derives:

  cells.csv            merged matrix in tidy form
  gold_credit.csv      per-gold credit: column SUM (clipped to 1) and column MAX
  coverage_topic.csv   per-(generator, topic) coverage under both rules
  validity.csv         per-generation raw matched-vote share (precision input)
  precision_topic.csv  per-(generator, topic) mean validity

Coverage default downstream is the SUM rule (matches the Aggregation section
and the supervisor's worked examples); the MAX column implements the Recall
section's alternative so the two can be compared. See README.

Usage:
  python aggregate.py --verdicts verdicts.jsonl --topics topics.json \
      --panels panels.json --out out/ [--panel disjoint|full]
"""
import argparse
from pathlib import Path

from bweird.analysis import aggregate_all, load_panels, load_topics, load_verdicts, log

# Repo-root-relative defaults, resolved from this file so the stage runs from
# any working directory. Every path can still be overridden on the command line.
ROOT = Path(__file__).resolve().parent.parent
ADAPTED = ROOT / "results" / "adapted"
AGG = ROOT / "results" / "agg"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verdicts", default=str(ADAPTED / "verdicts.jsonl"))
    ap.add_argument("--topics", default=str(ADAPTED / "topics.json"))
    ap.add_argument("--panels", default=str(ADAPTED / "panels.json"))
    ap.add_argument("--out", default=str(AGG))
    ap.add_argument("--panel", choices=["disjoint", "full"], default="disjoint",
                    help="disjoint = family-disjoint scoring panel (default); "
                         "full = base panel incl. own-family judge (bias analysis only)")
    args = ap.parse_args()

    topics = load_topics(args.topics)
    panels = load_panels(args.panels)
    verdicts = load_verdicts(args.verdicts, topics)

    res = aggregate_all(verdicts, topics, panels, config=args.panel)

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    suffix = "" if args.panel == "disjoint" else "_full"
    for name in ("cells", "gold_credit", "coverage_topic", "validity",
                 "precision_topic"):
        res[name].to_csv(out / f"{name}{suffix}.csv", index=False)

    cov = res["coverage_topic"]
    log.info("aggregated %d generators x %d topics (panel=%s)",
             cov.generator.nunique(), cov.topic_id.nunique(), args.panel)
    summary = (cov.groupby("generator")[["coverage_sum", "coverage_max"]]
               .mean().round(3).sort_values("coverage_sum", ascending=False))
    print("\nMean topic coverage per generator (sum rule vs max rule):")
    print(summary.to_string())
    print(f"\nArtifacts written to {out}/")


if __name__ == "__main__":
    main()
