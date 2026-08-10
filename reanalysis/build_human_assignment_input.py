"""Build the human-annotation input that human_assignment_audit.py expects.

The audit script wants one unambiguous human label per item, in the columns
``generator, topic, gen_index, label``. The annotation sheet does not ship in
that shape: ``results/annotation/annotations_adjudicated.csv`` carries two
independent annotators plus an ``adjudicated`` column that is populated only
where the two agreed (161 of 200 rows).

We take the adjudicated column as the human label, so the audit runs on the
subset where the annotators agreed with each other. That is a methodological
choice, not a neutral format conversion: the annotation protocol did not
specify how to resolve disagreement, and restricting to agreed items makes the
resulting agreement figure conditional on inter-annotator consensus. It must be
reported as such. The 39 discordant rows are excluded, not adjudicated.

Run from the repo root:  python reanalysis/build_human_assignment_input.py
"""
import sys
from pathlib import Path

import pandas as pd

SRC = Path(__file__).parent.parent / "results" / "annotation" / "annotations_adjudicated.csv"
DST = Path(__file__).parent.parent / "results" / "annotation" / "human_annotations.csv"


def main():
    """Write the agreed-annotator subset in the audit script's input shape."""
    if not SRC.exists():
        raise SystemExit(f"{SRC} not found; run 9_merge_annotation.py first.")
    src = pd.read_csv(SRC)
    agreed = src[src.adjudicated.notna()].copy()

    out = pd.DataFrame({
        "generator": agreed.generator,
        "topic": agreed.topic_id,
        "gen_index": agreed.generation_id,
        "label": agreed.adjudicated.astype(int),
    })
    out.to_csv(DST, index=False)

    n_disagree = len(src) - len(agreed)
    print(f"{len(src)} annotated items, {len(agreed)} with both annotators agreeing "
          f"({len(agreed) / len(src):.1%}), {n_disagree} discordant and excluded.")
    print(f"wrote {DST}")
    if len(agreed) != 161:
        print(f"NOTE: expected 161 agreed items, got {len(agreed)}; the figures "
              f"quoted in Results 4.6 were computed at 161.", file=sys.stderr)


if __name__ == "__main__":
    main()
