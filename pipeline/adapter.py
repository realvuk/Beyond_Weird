#!/usr/bin/env python3
"""
adapter.py — bridge the BWEIRD harness outputs to the eval-script contract.

Reads (native harness formats):
  data/gold_standard.json        v2 gold: topics carry topic_id, pair_id, arm,
                                  population, and perspectives[] each with a
                                  canonical perspective_id (authoritative for
                                  gold order — match_gold_id indexes into it)
  data/outputs/judgments.jsonl   judge verdicts, one per (judge x generation)
  config/judges.json             {"panel":[...], "substitutes":{...}}

Writes (eval-script formats, into --out):
  verdicts.jsonl   {generator, topic_id, generation_id, judge, match, status}
  topics.json      {"topics":[{topic_id, pair_id, arm, gold_ids}]}
  panels.json      {families, base_panel, substitutions}

Field mapping (from inspection of the harness output):
  generator     <- generator_slug
  judge         <- judge_slug
  generation_id <- "gen_%d" % gen_index
  match/status  <- match_gold_id:  1..5 -> perspectives[i-1].perspective_id, "ok"
                                     0   -> None (real no-match),             "ok"
                                     null-> None,                             "error"
  topics/pairs/arms/gold_ids <- read directly from gold_standard.json
                                (gold_ids in the file's native order)

data/topics.json is NOT read: gold_standard.json is the single source of
truth for topic ids, pairing, arm, and gold order. Nothing is modified.

Run:  python adapter.py --root . --out results/adapted
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def build_topics(gold: dict):
    """gold_standard.json -> ({"topics":[...]}, {topic_id: [ordered gold ids]})."""
    if "topics" not in gold:
        raise SystemExit("gold_standard.json has no 'topics' key")
    topics, gold_by_topic = [], {}
    for t in gold["topics"]:
        tid = t["topic_id"]
        persp = t["perspectives"]
        gold_ids = []
        for i, p in enumerate(persp, 1):
            gid = p.get("perspective_id")
            if not gid:
                raise SystemExit(
                    f"topic {tid} perspective {i} missing 'perspective_id'")
            gold_ids.append(str(gid))
        topics.append({
            "topic_id": tid,
            "pair_id": t["pair_id"],          # int in v2; carried through as-is
            "arm": str(t["arm"]).lower(),
            "gold_ids": gold_ids,
        })
        gold_by_topic[tid] = gold_ids
    return {"topics": topics}, gold_by_topic


def convert_verdicts(path: Path, gold_by_topic: dict):
    rows, skipped = [], 0
    counts = defaultdict(Counter)
    status = Counter()
    families = {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            tid = r["topic_id"]
            if tid not in gold_by_topic:
                skipped += 1
                continue
            golds = gold_by_topic[tid]
            mgid = r.get("match_gold_id")
            if mgid is None:
                match, st = None, "error"
            elif mgid == 0:
                match, st = None, "ok"
            else:
                if not (1 <= mgid <= len(golds)):
                    raise SystemExit(
                        f"match_gold_id {mgid} out of range for {tid} "
                        f"({len(golds)} golds)")
                match, st = golds[mgid - 1], "ok"
            gen, judge = r["generator_slug"], r["judge_slug"]
            rows.append({"generator": gen, "topic_id": tid,
                         "generation_id": f"gen_{r['gen_index']}",
                         "judge": judge, "match": match, "status": st})
            counts[gen][judge] += 1
            status[st] += 1
            families[gen] = r.get("generator_family", families.get(gen))
            families[judge] = r.get("judge_family", families.get(judge))
    return rows, counts, status, skipped, families


def convert_panels(cfg: dict, families_seen: dict):
    families = dict(families_seen)
    base = []
    for j in cfg["panel"]:
        families[j["slug"]] = j["family"]
        base.append(j["slug"])
    subs = {}
    for fam, s in cfg["substitutes"].items():
        families[s["slug"]] = s["family"]
        subs[fam] = s["slug"]
    return {"families": families, "base_panel": base, "substitutions": subs}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".")
    ap.add_argument("--out", default="results/adapted")
    ap.add_argument("--gold", default="data/gold_standard.json")
    ap.add_argument("--judgments", default="data/outputs/judgments.jsonl")
    ap.add_argument("--judges-config", default="config/judges.json")
    args = ap.parse_args()

    root = Path(args.root)
    out = root / args.out
    out.mkdir(parents=True, exist_ok=True)

    gold = _load(root / args.gold)
    cfg = _load(root / args.judges_config)

    topics_obj, gold_by_topic = build_topics(gold)
    rows, counts, status, skipped, families = convert_verdicts(
        root / args.judgments, gold_by_topic)
    panels = convert_panels(cfg, families)

    with open(out / "verdicts.jsonl", "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    (out / "topics.json").write_text(
        json.dumps(topics_obj, indent=2, ensure_ascii=False), encoding="utf-8")
    (out / "panels.json").write_text(
        json.dumps(panels, indent=2, ensure_ascii=False), encoding="utf-8")

    ts = topics_obj["topics"]
    nweird = sum(t["arm"] == "weird" for t in ts)
    print(f"topics: {len(ts)} ({nweird} weird / {len(ts)-nweird} serbian)")
    pairs = Counter(t["pair_id"] for t in ts)
    bad = {p: n for p, n in pairs.items() if n != 2}
    if bad:
        print(f"  WARNING: pairs without exactly 2 arms: {bad}", file=sys.stderr)
    badg = {t["topic_id"]: len(t["gold_ids"]) for t in ts if len(t["gold_ids"]) != 5}
    if badg:
        print(f"  WARNING: topics without 5 golds: {badg}", file=sys.stderr)
    print(f"verdicts: {len(rows)} written, {skipped} skipped (unknown topic)")
    print(f"  status: {dict(status)}")
    print(f"panels: {len(panels['base_panel'])} base judges, "
          f"{len(panels['substitutions'])} sub rows, "
          f"{len(panels['families'])} models in families map")

    print("\nper-generator judge counts (verify each generator's 5-family panel):")
    judges = sorted({j for c in counts.values() for j in c})
    print(f"  {'generator':38s} " + " ".join(f"{j.split('/')[-1][:9]:>9s}" for j in judges))
    fam = panels["families"]
    for gen in sorted(counts):
        gfam = fam.get(gen)
        cells = []
        for j in judges:
            n = counts[gen].get(j, 0)
            # flag: own-family judge with nonzero count = family leak
            flag = "!" if (n and fam.get(j) == gfam and gen != j) else " "
            cells.append(f"{n:>8d}{flag}")
        print(f"  {gen:38s} " + " ".join(cells))
    print("\n  '!' = a judge sharing the generator's family scored it "
          "(should be 0 under family-disjointness).")
    print("  A generator's own-family BASE judge should read 0; its SUBSTITUTE "
          "carries those rows instead.")
    print(f"\nwrote -> {out}/verdicts.jsonl, topics.json, panels.json")


if __name__ == "__main__":
    main()
