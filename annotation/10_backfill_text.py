#!/usr/bin/env python3
"""
10_backfill_text.py  (v2)  --  fill generated-perspective text into an existing
annotation_blind.csv, aligning the gen_index bases of judgments vs generations.

v2 change: judgments.jsonl may number generations 1..N (1-based) while
generations.jsonl numbers them 0..N-1 (0-based), or vice versa. Joining them
straight across silently shifts every row by one and drops the top index. This
version detects the base of each source and applies the offset, and BLANKS any
row it cannot fill so a re-run never leaves stale (wrong) text behind.
"""
import argparse
import csv
import json
import sys


def g(d, *keys):
    for k in keys:
        if k in d and d[k] not in (None, ""):
            return d[k]
    return None

def load_records(path):
    txt = open(path, encoding="utf-8").read().strip()
    if not txt:
        return
    if txt.lstrip()[0] != "[":
        recs, ok = [], True
        for line in txt.splitlines():
            line = line.strip()
            if not line:
                continue
            try: recs.append(json.loads(line))
            except json.JSONDecodeError: ok = False; break
        if ok:
            yield from recs; return
    data = json.loads(txt)
    yield from (data if isinstance(data, list) else [data])

def build_map(path):
    m = {}; pairs = set(); layout = None; idxs = set()
    for rec in load_records(path):
        gen = g(rec, "generator_slug", "generator", "model_slug", "model")
        tid = g(rec, "topic_id", "topic")
        if gen is None or tid is None:
            continue
        pairs.add((gen, tid))
        persps = g(rec, "perspectives", "generations", "outputs")
        if isinstance(persps, list):
            layout = layout or "nested(0-based enumerate)"
            for i, p in enumerate(persps):
                if isinstance(p, dict):
                    m[(gen, tid, i)] = {"summary": g(p,"summary","generated_summary") or "",
                                        "explanation": g(p,"explanation","generated_explanation","text") or ""}
                    idxs.add(i)
        else:
            layout = layout or "flat(explicit index)"
            gi = g(rec, "gen_index", "generation_index", "index", "idx")
            if gi is None:
                continue
            gi = int(gi); idxs.add(gi)
            m[(gen, tid, gi)] = {"summary": g(rec,"summary","generated_summary") or "",
                                 "explanation": g(rec,"explanation","generated_explanation","text") or ""}
    return m, pairs, layout, (min(idxs) if idxs else None), (max(idxs) if idxs else None)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--generations", required=True)
    ap.add_argument("--key",   default="results/annotation/annotation_key.csv")
    ap.add_argument("--blind", default="results/annotation/annotation_blind.csv")
    ap.add_argument("--out",   default="results/annotation/annotation_blind.csv")
    ap.add_argument("--offset", type=int, default=None,
                    help="generation_index = key_gen_index + offset. Default: auto-detect.")
    args = ap.parse_args()

    gmap, pairs, layout, gmin, gmax = build_map(args.generations)
    key = {r["sample_id"]: r for r in csv.DictReader(open(args.key, encoding="utf-8"))}
    with open(args.blind, encoding="utf-8") as f:
        rd = csv.DictReader(f); rows = list(rd); cols = rd.fieldnames

    key_idxs = [int(key[r["sample_id"]]["gen_index"]) for r in rows if r["sample_id"] in key]
    kmin, kmax = min(key_idxs), max(key_idxs)
    offset = args.offset if args.offset is not None else (gmin - kmin)
    print(f"generation layout: {layout}; generation index range [{gmin}..{gmax}], "
          f"key gen_index range [{kmin}..{kmax}]")
    print(f"applied offset: generation_index = key_gen_index + ({offset})  "
          f"{'(auto-detected)' if args.offset is None else '(manual)'}")

    filled = 0; miss_pair = []; miss_index = []
    for r in rows:
        k = key.get(r["sample_id"])
        if not k:
            continue
        gen, tid, gi = k["generator"], k["topic_id"], int(k["gen_index"]) + offset
        hit = gmap.get((gen, tid, gi))
        if hit:
            r["generated_summary"] = hit["summary"]
            r["generated_explanation"] = hit["explanation"]
            filled += 1
        else:
            r["generated_summary"] = ""; r["generated_explanation"] = ""   # blank stale text
            (miss_pair if (gen, tid) not in pairs else miss_index).append(
                (r["sample_id"], gen, tid, gi))

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)

    print(f"\nfilled {filled}/{len(rows)} rows.")
    if miss_pair:
        print(f"!! {len(miss_pair)} rows: (generator,topic) not in generations (id mismatch). "
              f"e.g. {miss_pair[:3]}", file=sys.stderr)
    if miss_index:
        print(f"!! {len(miss_index)} rows: index still out of range after offset. "
              f"e.g. {miss_index[:3]}", file=sys.stderr)
    if not miss_pair and not miss_index:
        print("all rows filled. SPOT-CHECK one row against the actual generation to confirm "
              "the alignment (pick a sample_id, look up its generator/topic/gen_index).")
    print(f"wrote -> {args.out}")

if __name__ == "__main__":
    main()
