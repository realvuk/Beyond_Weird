#!/usr/bin/env python3
"""
7_sample_for_annotation.py

Draw the human-validation sample for the reliability section, stratified by
panel agreement and (by default) balanced across the WEIRD / Serbian arms.

Why this exists
---------------
Soft vote-share aggregation removes the *calibration* use of human labels
(there is no threshold to tune), but NOT the *validation* use. Inter-judge
agreement (kappa / AC1 / alpha) measures whether the judges agree with each
other, not whether they are right; a correlated panel can agree and be wrong in
the same direction. The judge panel is itself an LLM system and this paper's
claim is that LLMs can carry cultural bias, so the instrument must be checked
against humans on BOTH arms before its coverage numbers -- and the WEIRD-gap
null in particular -- can be trusted. This script selects the generations a
pair of annotators will label; 5_eval_reliability.py consumes the labels.

Selection logic
---------------
For each generated perspective, match_share = (judges matching it to any gold)
/ (judges that voted). With five judges this lands on {0, .2, .4, .6, .8, 1}.
Stratify on it, then:
  s0 (match_share == 0, confident no-match)  -> take in full up to --s0-cap.
        This is the false-negative check that makes coverage a lower bound.
  s2 (contested, ~.4/.6)                      -> oversample (the least-sure
        decisions, the ones the operating point used to hinge on).
  s1/s3/s4 (near-confident + confident match) -> lighter samples.
With --balance-arms (default) each stratum is filled as evenly as possible from
the two arms so per-arm validity has comparable power.

Outputs (into --out)
--------------------
  annotation_blind.csv : the annotators' sheet. One row per generation,
        shuffled, opaque sample_id, topic + population + gold SUMMARIES + the
        generated perspective. NO panel decision, NO agreement weight. Empty
        annotator_1 / annotator_2 columns.
  annotation_key.csv   : hidden provenance (sample_id -> generator, topic_id,
        gen_index, arm, match_share, stratum, panel_modal_gold). Kept OUT of the
        annotators' sheet; join on sample_id after labelling.
  gold_legend.csv      : per-topic full gold text for the annotators to consult.

annotation_key.csv is computed from judgments.jsonl alone, so the selection is
reproducible even before the generated-text join is wired up.
"""
import argparse
import csv
import json
import os
import random
from collections import Counter, defaultdict

STRATA = ["s0_nomatch", "s1_lean_nomatch", "s2_contested", "s3_lean_match", "s4_match"]

def stratum_of(ms):
    if ms is None:        return None
    if ms <= 0.0:         return "s0_nomatch"
    if ms < 0.3:          return "s1_lean_nomatch"
    if ms < 0.7:          return "s2_contested"
    if ms < 1.0:          return "s3_lean_match"
    return "s4_match"

def load_gold(path):
    with open(path) as f:
        data = json.load(f)
    topics = {}
    for t in data["topics"]:
        persps = [{
            "id": i,
            "summary": p.get("summary", ""),
            "explanation": p.get("explanation", ""),
        } for i, p in enumerate(t["perspectives"], start=1)]
        topics[t["topic_id"]] = {
            "arm": t.get("arm", ""),
            "topic_title": t.get("topic_title", ""),
            "population": t.get("population", ""),
            "perspectives": persps,
        }
    return topics

def load_generations(path):
    gens = {}
    if not path:
        return gens
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            g = r.get("generator_slug") or r.get("generator")
            tid = r.get("topic_id")
            gi = r.get("gen_index", r.get("generation_index"))
            summ = r.get("summary") or r.get("generated_summary") or ""
            expl = r.get("explanation") or r.get("generated_explanation") or ""
            if g is not None and tid is not None and gi is not None:
                gens[(g, tid, int(gi))] = (summ, expl)
    return gens

def per_generation_stats(path):
    acc = defaultdict(lambda: {"present": 0, "matched": 0, "golds": Counter()})
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            g = r.get("generator_slug") or r.get("generator")
            tid = r.get("topic_id")
            gi = r.get("gen_index", r.get("generation_index"))
            mg = r.get("match_gold_id", None)
            if g is None or tid is None or gi is None:
                continue
            if mg is None:            # error / abstention: judge did not vote
                continue
            key = (g, tid, int(gi))
            acc[key]["present"] += 1
            if int(mg) != 0:
                acc[key]["matched"] += 1
                acc[key]["golds"][int(mg)] += 1
    out = {}
    for key, v in acc.items():
        present = v["present"]
        ms = (v["matched"] / present) if present > 0 else None
        modal = v["golds"].most_common(1)[0][0] if v["golds"] else 0
        out[key] = {"present": present, "match_share": ms,
                    "modal_gold": modal, "stratum": stratum_of(ms)}
    return out

def take(items, tgt, balance, rng):
    """items: list of (key, arm). Return up to tgt, arm-balanced if requested."""
    if tgt <= 0 or not items:
        return []
    if not balance:
        pool = items[:]
        rng.shuffle(pool)
        return pool[:tgt]
    by_arm = defaultdict(list)
    for it in items:
        by_arm[it[1]].append(it)
    for a in by_arm:
        rng.shuffle(by_arm[a])
    arms = sorted(by_arm)                       # deterministic order
    idx = {a: 0 for a in arms}
    picked = []
    while len(picked) < tgt and any(idx[a] < len(by_arm[a]) for a in arms):
        for a in arms:                          # round-robin -> even split, auto top-up
            if len(picked) >= tgt:
                break
            if idx[a] < len(by_arm[a]):
                picked.append(by_arm[a][idx[a]])
                idx[a] += 1
    return picked

def render_options(persps):
    return " | ".join(f"[{p['id']}] {p['summary']}" for p in persps)

def main():
    ap = argparse.ArgumentParser(description="Stratified annotation sampler for panel validation.")
    ap.add_argument("--judgments", default="data/outputs/judgments.jsonl",
                    help="cleaned native judgments.jsonl (family-disjoint).")
    ap.add_argument("--gold", default="data/gold_standard.json")
    ap.add_argument("--generations", default=None,
                    help="optional jsonl of generated perspectives, keyed by "
                         "(generator_slug, topic_id, gen_index). If omitted, the "
                         "blind sheet leaves generated text blank but selection + key still write.")
    ap.add_argument("--out", default="results/annotation")
    ap.add_argument("--s0-cap", type=int, default=60, help="max confident-no-match rows (s0).")
    ap.add_argument("--scale", type=float, default=1.0, help="scale all non-s0 targets.")
    ap.add_argument("--no-balance", action="store_true", help="disable arm balancing.")
    ap.add_argument("--seed", type=int, default=20260721)
    args = ap.parse_args()

    balance = not args.no_balance
    rng = random.Random(args.seed)
    os.makedirs(args.out, exist_ok=True)

    topics = load_gold(args.gold)
    gens = load_generations(args.generations)
    stats = per_generation_stats(args.judgments)

    targets = {
        "s1_lean_nomatch": int(round(25 * args.scale)),
        "s2_contested":    int(round(70 * args.scale)),
        "s3_lean_match":   int(round(25 * args.scale)),
        "s4_match":        int(round(20 * args.scale)),
    }

    pool = defaultdict(list)
    dropped_no_topic = 0
    for key, st in stats.items():
        _, tid, _ = key
        if tid not in topics:
            dropped_no_topic += 1
            continue
        if st["stratum"] is None:
            continue
        pool[st["stratum"]].append((key, topics[tid]["arm"]))

    chosen = []
    for s in STRATA:
        items = pool.get(s, [])
        tgt = min(args.s0_cap, len(items)) if s == "s0_nomatch" else targets.get(s, 0)
        sel = take(items, tgt, balance, rng)
        chosen += [(k, a, s) for (k, a) in sel]
    rng.shuffle(chosen)

    # ---- report: arm x stratum crosstab (available vs selected) ----
    avail = Counter((s, a) for s in pool for (_, a) in pool[s])
    picked = Counter((s, a) for (_, a, s) in chosen)
    arms = sorted({a for (_, a, _) in chosen} | {a for (s, a) in avail})
    print(f"generations with match_share: {sum(len(v) for v in pool.values())}"
          f"  (dropped, topic not in gold: {dropped_no_topic})")
    print(f"\n{'stratum':<18} " + "  ".join(f"{a:>16}" for a in arms) + "     total")
    for s in STRATA:
        cells = "  ".join(f"{picked[(s,a)]:>3}/{avail[(s,a)]:<12}" for a in arms)
        tot = sum(picked[(s, a)] for a in arms)
        print(f"{s:<18} {cells}   {tot:>5}")
    print(f"{'SELECTED TOTAL':<18} " + " " * (18 * len(arms)) + f"{len(chosen):>7}")

    # ---- write outputs ----
    blind_p = os.path.join(args.out, "annotation_blind.csv")
    key_p   = os.path.join(args.out, "annotation_key.csv")
    leg_p   = os.path.join(args.out, "gold_legend.csv")

    with open(blind_p, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["sample_id", "topic_id", "topic_title", "population",
                    "gold_options", "generated_summary", "generated_explanation",
                    "annotator_1", "annotator_2", "notes"])
        for i, (key, _arm, _s) in enumerate(chosen, start=1):
            g, tid, gi = key
            sid = f"A{i:04d}"
            t = topics[tid]
            summ, expl = gens.get(key, ("", ""))
            w.writerow([sid, tid, t["topic_title"], t["population"],
                        render_options(t["perspectives"]), summ, expl, "", "", ""])

    with open(key_p, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["sample_id", "generator", "topic_id", "gen_index", "arm",
                    "present_judges", "match_share", "stratum", "panel_modal_gold"])
        for i, (key, arm, s) in enumerate(chosen, start=1):
            g, tid, gi = key
            st = stats[key]
            w.writerow([f"A{i:04d}", g, tid, gi, arm,
                        st["present"], f"{st['match_share']:.3f}", s, st["modal_gold"]])

    with open(leg_p, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["topic_id", "topic_title", "population", "gold_id",
                    "gold_summary", "gold_explanation"])
        for tid, t in topics.items():
            for p in t["perspectives"]:
                w.writerow([tid, t["topic_title"], t["population"],
                            p["id"], p["summary"], p["explanation"]])

    print(f"\nwrote -> {blind_p}\n         {key_p}\n         {leg_p}")
    if not gens:
        print("NOTE: no --generations given, generated_summary/explanation are blank. "
              "Point --generations at the generation output to fill them.")

if __name__ == "__main__":
    main()
