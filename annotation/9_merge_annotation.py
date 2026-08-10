#!/usr/bin/env python3
"""
9_merge_annotations.py  --  bridge the completed annotation sheet to 5_eval_reliability.py.

Joins the two annotators' filled blind sheet to the hidden key on sample_id and
writes the labelled CSV the reliability step consumes. Rows where the annotators
agree are auto-adjudicated; rows where they disagree are left blank in
`adjudicated` and listed for manual resolution by discussion (the paper's stated
procedure). Also previews raw inter-annotator agreement (the eventual human
ceiling) so you can sanity-check before running the full reliability script.

Inputs are the sampler's own outputs:
  annotation_blind.csv : sample_id, ..., annotator_1, annotator_2, notes   (now filled)
  annotation_key.csv   : sample_id, generator, topic_id, gen_index, arm,
                         present_judges, match_share, stratum, panel_modal_gold
"""
import argparse
import csv
import sys

VALID = {"0", "1", "2", "3", "4", "5"}

def norm(x):
    """Normalise a label cell: '', '3', or '3.0' -> '' or '3'. Returns (value, ok)."""
    s = (x or "").strip()
    if s == "":
        return "", True
    if s.endswith(".0"):
        s = s[:-2]
    return s, (s in VALID)

def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--blind", default="results/annotation/annotation_blind.csv")
    ap.add_argument("--key",   default="results/annotation/annotation_key.csv")
    ap.add_argument("--out",   default="results/annotation/annotations_adjudicated.csv")
    args = ap.parse_args()

    blind = {r["sample_id"]: r for r in read_csv(args.blind)}
    key   = {r["sample_id"]: r for r in read_csv(args.key)}

    missing_in_key = set(blind) - set(key)
    if missing_in_key:
        print(f"WARNING {len(missing_in_key)} blind rows have no key entry (ignored): "
              f"{sorted(missing_in_key)[:5]}...", file=sys.stderr)

    rows, both_labelled, agree = [], 0, 0
    disagreements, unlabelled, bad = [], [], []
    for sid in sorted(key):
        k = key[sid]
        b = blind.get(sid)
        a1_raw = b.get("annotator_1", "") if b else ""
        a2_raw = b.get("annotator_2", "") if b else ""
        a1, ok1 = norm(a1_raw)
        a2, ok2 = norm(a2_raw)
        if not ok1 or not ok2:
            bad.append((sid, a1_raw, a2_raw))
        if a1 == "" or a2 == "":
            unlabelled.append(sid)
            adjudicated = ""
        else:
            both_labelled += 1
            if a1 == a2:
                agree += 1
                adjudicated = a1
            else:
                adjudicated = ""
                disagreements.append((sid, k["arm"], a1, a2, k["panel_modal_gold"]))
        rows.append({
            "sample_id": sid,
            "generator": k["generator"],
            "topic_id": k["topic_id"],
            "generation_id": k["gen_index"],   # rename to match 5_eval_reliability's expected column
            "arm": k["arm"],
            "match_share": k["match_share"],
            "stratum": k["stratum"],
            "panel_modal_gold": k["panel_modal_gold"],
            "annotator_1": a1,
            "annotator_2": a2,
            "adjudicated": adjudicated,
        })

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print(f"rows: {len(rows)}   both-labelled: {both_labelled}   "
          f"unlabelled: {len(unlabelled)}")
    if both_labelled:
        print(f"raw inter-annotator agreement (preview of human ceiling): "
              f"{agree}/{both_labelled} = {agree/both_labelled:.1%}")
    print(f"auto-adjudicated (annotators agree): {agree}")
    print(f"NEED MANUAL RESOLUTION (disagreements): {len(disagreements)}")
    if bad:
        print(f"\n!! {len(bad)} rows have out-of-range labels (must be 0-5): {bad[:5]}",
              file=sys.stderr)
    if unlabelled:
        print(f"!! {len(unlabelled)} rows not yet labelled by both annotators "
              f"(adjudicated left blank).", file=sys.stderr)
    if disagreements:
        print("\nresolve these by discussion, then fill `adjudicated` in the output CSV:")
        print(f"  {'sample_id':<10}{'arm':<10}{'ann_1':>6}{'ann_2':>6}{'panel':>7}")
        for sid, arm, a1, a2, pm in disagreements[:40]:
            print(f"  {sid:<10}{arm:<10}{a1:>6}{a2:>6}{pm:>7}")
        if len(disagreements) > 40:
            print(f"  ... and {len(disagreements)-40} more (see CSV rows with blank adjudicated)")
    print(f"\nwrote -> {args.out}")
    print("Fill any blank `adjudicated` cells, then feed this file to 5_eval_reliability.py.")

if __name__ == "__main__":
    main()
