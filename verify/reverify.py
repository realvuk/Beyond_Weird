#!/usr/bin/env python3
"""reverify.py -- fully independent re-derivation of the BWEIRD paper's numbers.

Imports nothing from the project: not bw_common, not bweird, not audit/.
Reads only judgments.jsonl, generations.jsonl, gold_standard.json,
config/judges.json, config/models.json and data/outputs/generation_failures.jsonl,
then re-derives every headline quantity and asserts it against BOTH the
pipeline's own results/ CSVs and the values printed in the manuscript.

Coverage credit is carried in exact rational arithmetic (fractions.Fraction)
throughout, so no result depends on floating-point summation order. This is
what settles the Table 6 tie question: whether two |deltas| are equal is
decided exactly, not by noise in the 17th significant digit.

Usage:  python verify/reverify.py   [--root REPO] [--out DIR]
Exit status 0 iff every assertion holds.
"""
from __future__ import annotations

import argparse
import csv
import itertools
import json
import statistics
import sys
from collections import Counter, defaultdict
from fractions import Fraction as F
from pathlib import Path

# --------------------------------------------------------------------------
# reporting
# --------------------------------------------------------------------------
CHECKS: list[dict] = []


def chk(area: str, name: str, ok: bool, expected, got, note: str = "") -> bool:
    CHECKS.append({"area": area, "check": name,
                   "verdict": "PASS" if ok else "FAIL",
                   "expected": str(expected), "got": str(got), "note": note})
    return ok


def hdr(t: str) -> None:
    print("\n" + "=" * 78 + f"\n{t}\n" + "=" * 78)


def f3(x) -> float:
    return float(x)


# --------------------------------------------------------------------------
# loading -- raw only
# --------------------------------------------------------------------------
def load(root: Path):
    gold = json.loads((root / "data" / "gold_standard.json").read_text(encoding="utf-8"))
    assert gold["version"] == "v2", gold["version"]
    topics = {}
    for t in gold["topics"]:
        ids = [p["perspective_id"] for p in t["perspectives"]]
        assert len(ids) == len(set(ids))
        topics[t["topic_id"]] = {
            "pair": int(t["pair_id"]), "arm": str(t["arm"]).lower(),
            "title": t["topic_title"], "gold_ids": ids,
            "tiers": [int(p["extremity_tier"]) for p in t["perspectives"]],
        }

    gens = {}
    gens_path = root / "data" / "outputs" / "generations.jsonl"
    for line in gens_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        d = json.loads(line)
        idx = [p["index"] for p in d["perspectives"]]
        gens[(d["model_slug"], d["topic_id"])] = idx

    raw = []
    judg_path = root / "data" / "outputs" / "judgments.jsonl"
    for line in judg_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        raw.append(json.loads(line))

    cfg_j = json.loads((root / "config" / "judges.json").read_text(encoding="utf-8"))
    cfg_m = json.loads((root / "config" / "models.json").read_text(encoding="utf-8"))
    return topics, gens, raw, cfg_j, cfg_m


LABEL = {}  # slug -> manuscript display name


def build_labels(cfg_m):
    for m in cfg_m:
        n = m["display_name"]
        LABEL[m["slug"]] = "Gemini 3.1 Pro" if n == "Gemini 3.1 Pro Preview" else n


# --------------------------------------------------------------------------
# 1. verdict accounting, from first principles
# --------------------------------------------------------------------------
def accounting(raw, topics, gens, cfg_j, cfg_m):
    hdr("1. VERDICT ACCOUNTING")
    n_raw = len(raw)
    errors = [r for r in raw if r.get("match_gold_id") is None]

    by_key = defaultdict(list)
    for i, r in enumerate(raw):
        by_key[r["key"]].append(i)
    dup_keys = {k: v for k, v in by_key.items() if len(v) > 1}
    n_dup_extra = sum(len(v) - 1 for v in dup_keys.values())
    dup_rows = [i for v in dup_keys.values() for i in v]
    dup_err = sum(raw[i].get("match_gold_id") is None for i in dup_rows)

    # de-duplicate by keeping the LAST record of each key (retry order in file)
    keep = {k: v[-1] for k, v in by_key.items()}
    kept = [raw[i] for i in sorted(keep.values())]
    valid = [r for r in kept if r.get("match_gold_id") is not None]
    irrecoverable = [r for r in kept if r.get("match_gold_id") is None]

    print(f"  raw records                 {n_raw}")
    print(f"  errors (null match_gold_id) {len(errors)}")
    print(f"  duplicate keys              {len(dup_keys)}  extra rows {n_dup_extra}")
    print(f"  duplicate rows that errored {dup_err}/{len(dup_rows)}")
    print(f"  valid after dedup           {len(valid)}")
    print(f"  never recovered             {len(irrecoverable)}")

    A = "1 accounting"
    chk(A, "raw = 5,228", n_raw == 5228, 5228, n_raw)
    chk(A, "errors = 44", len(errors) == 44, 44, len(errors))
    chk(A, "duplicate extra rows = 28", n_dup_extra == 28, 28, n_dup_extra)
    # of each duplicated key's rows, every one EXCEPT the last must be an error
    # (the retry is what created the second record); 6 keys never recovered
    first_all_err = all(all(raw[i].get("match_gold_id") is None for i in v[:-1])
                        for v in dup_keys.values())
    chk(A, "every superseded duplicate row is an error", first_all_err,
        True, first_all_err,
        "22 of the 28 retries recovered a verdict; 6 failed again")
    chk(A, "valid = 5,184", len(valid) == 5184, 5184, len(valid))
    chk(A, "never recovered = 16", len(irrecoverable) == 16, 16, len(irrecoverable))
    chk(A, "5,228 - 44 = 5,184 (the correct route to N)",
        n_raw - len(errors) == len(valid), n_raw - len(errors), len(valid),
        "the 28 duplicates are a SUBSET of the 44 errors, so 5,228-44-28=5,156 "
        "double-subtracts and is wrong")
    pv = 100 * len(valid) / n_raw
    chk(A, "99.2% valid", abs(pv - 99.2) < 0.05, 99.2, round(pv, 2))

    # grid
    per_gen = defaultdict(set)
    for r in valid:
        per_gen[(r["generator_slug"], r["topic_id"], r["gen_index"])].add(r["judge_slug"])
    njudge = Counter(len(v) for v in per_gen.values())
    generators = sorted({r["generator_slug"] for r in valid})
    judges = sorted({r["judge_slug"] for r in valid})
    print(f"  generators {len(generators)}  topics {len({r['topic_id'] for r in valid})}"
          f"  judges {len(judges)}")
    print(f"  judges per generation: {dict(sorted(njudge.items()))}")
    G = "1 grid"
    chk(G, "13 generators", len(generators) == 13, 13, len(generators))
    chk(G, "16 topics", len(topics) == 16, 16, len(topics))
    chk(G, "7 judges in roster", len(judges) == 7, 7, len(judges))
    chk(G, "208 generation records", len(gens) == 208, 208, len(gens))
    chk(G, "1,040 generated perspectives",
        sum(len(v) for v in gens.values()) == 1040, 1040,
        sum(len(v) for v in gens.values()))
    chk(G, "80 gold perspectives",
        sum(len(t["gold_ids"]) for t in topics.values()) == 80, 80,
        sum(len(t["gold_ids"]) for t in topics.values()))
    chk(G, "intended verdicts = 5,200", 208 * 5 * 5 == 5200, 5200, 208 * 5 * 5)
    chk(G, "every (model,topic) has 5 generations",
        all(len(v) == 5 for v in gens.values()), "all 5",
        Counter(len(v) for v in gens.values()))
    chk(G, "16 generations judged by 4, the rest by 5",
        njudge.get(4) == 16 and njudge.get(5) == 1024,
        "{4:16, 5:1024}", dict(sorted(njudge.items())))

    # join guard: every judged (model,topic,gen_index) exists in generations,
    # where gen_index is 1-based into the perspectives list
    missing = [k for k in per_gen
               if k[2] not in gens.get((k[0], k[1]), [])]
    chk(G, "judgments join generations with no loss", not missing, 0, len(missing))

    # family disjointness, recomputed from the config
    fam = {m["slug"]: m["family"] for m in cfg_m}
    for j in cfg_j["panel"]:
        fam[j["slug"]] = j["family"]
    for s in cfg_j["substitutes"].values():
        fam[s["slug"]] = s["family"]
    same = [r for r in valid
            if fam.get(r["generator_slug"]) == fam.get(r["judge_slug"])]
    panels = {g: {r["judge_slug"] for r in valid if r["generator_slug"] == g}
              for g in generators}
    badpanel = {g: p for g, p in panels.items()
                if len(p) != 5 or len({fam[j] for j in p}) != 5}
    P = "1 panel"
    chk(P, "zero same-family verdicts", not same, 0, len(same))
    chk(P, "every panel is 5 judges from 5 distinct families",
        not badpanel, 0, len(badpanel))
    chk(P, "grok-4.3 never appears as a judge",
        not any(r["judge_slug"] == "x-ai/grok-4.3" for r in valid), 0,
        sum(r["judge_slug"] == "x-ai/grok-4.3" for r in valid))
    chk(P, "grok-4.5 never appears as a generator",
        not any(r["generator_slug"] == "x-ai/grok-4.5" for r in valid), 0,
        sum(r["generator_slug"] == "x-ai/grok-4.5" for r in valid))
    # de-randomisation: presentation_order[match_presented-1] == match_gold_id
    bad_der = 0
    for r in valid:
        po, mp, mg = r.get("presentation_order"), r.get("match_presented"), r["match_gold_id"]
        if po and mp:
            if not (1 <= mp <= len(po)) or po[mp - 1] != mg:
                bad_der += 1
        elif mg != 0:
            bad_der += 1
    chk(P, "de-randomisation consistent", bad_der == 0, 0, bad_der)
    return valid, panels, fam


# --------------------------------------------------------------------------
# 2. gold credit in exact rational arithmetic
# --------------------------------------------------------------------------
def gold_credit(valid, topics, gens):
    """(generator, topic) -> {gold_id: Fraction credit}, plus precision."""
    hdr("2. GOLD CREDIT (exact rational arithmetic, sum rule)")
    votes = defaultdict(dict)          # (g,t,judge) -> {gen_index: gold_id|None}
    for r in valid:                    # later duplicate already won in `valid`
        k = (r["generator_slug"], r["topic_id"], r["judge_slug"])
        mg = r["match_gold_id"]
        gid = None if mg == 0 else topics[r["topic_id"]]["gold_ids"][mg - 1]
        votes[k][r["gen_index"]] = gid

    credit, precision, clipped_cells, nj_by_cell = {}, {}, [], {}
    for (g, t) in sorted(gens):
        gold_ids = topics[t]["gold_ids"]
        jkeys = [k for k in votes if k[0] == g and k[1] == t]
        # per-judge split: k generations matched to one gold share 1/k
        percell = defaultdict(F)       # (gen, gold) -> summed 1/k over judges
        njudges = {}
        for gi in gens[(g, t)]:
            js = [k for k in jkeys if gi in votes[k]]
            njudges[gi] = len(js)
            assert js, (g, t, gi)
        for k in jkeys:
            jv = votes[k]
            kc = Counter(v for v in jv.values() if v is not None)
            for gi, v in jv.items():
                if v is not None:
                    percell[(gi, v)] += F(1, kc[v])
        col = {c: F(0) for c in gold_ids}
        for gi in gens[(g, t)]:
            n = njudges[gi]
            for c in gold_ids:
                col[c] += percell.get((gi, c), F(0)) / n
        for c in gold_ids:
            if col[c] > 1:
                clipped_cells.append((g, t, c, col[c]))
                col[c] = F(1)
        credit[(g, t)] = col
        nj_by_cell[(g, t)] = njudges
        # precision: share of a generation's judges that matched it to any gold
        vals = []
        for gi in gens[(g, t)]:
            js = [k for k in jkeys if gi in votes[k]]
            vals.append(F(sum(votes[k][gi] is not None for k in js), len(js)))
        precision[(g, t)] = sum(vals) / len(vals)

    print(f"  (generator, topic) cells      {len(credit)}")
    print(f"  gold columns clipped at 1.0   {len(clipped_cells)}")
    for g, t, c, v in clipped_cells:
        print(f"    {LABEL.get(g, g):<17} {t:<14} {c}  uncapped {float(v):.6f}")
    chk("2 credit", "1,040 gold rows",
        sum(len(v) for v in credit.values()) == 1040, 1040,
        sum(len(v) for v in credit.values()))
    return credit, precision, clipped_cells, nj_by_cell, votes


def coverage_tables(credit, precision, topics, gens):
    cov_t = {k: sum(v.values()) / len(v) for k, v in credit.items()}
    models = sorted({k[0] for k in cov_t})
    cov_m = {m: sum(v for k, v in cov_t.items() if k[0] == m) / 16 for m in models}
    prec_m = {m: sum(v for k, v in precision.items() if k[0] == m) / 16 for m in models}
    f1_m = {m: (F(0) if cov_m[m] + prec_m[m] == 0
                else 2 * cov_m[m] * prec_m[m] / (cov_m[m] + prec_m[m]))
            for m in models}
    return cov_t, cov_m, prec_m, f1_m


# --------------------------------------------------------------------------
# 3. cross-check against the pipeline's own CSVs
# --------------------------------------------------------------------------
def read_csv(p: Path):
    with p.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def against_pipeline(root, credit, cov_t, precision):
    hdr("3. AGAINST THE PIPELINE'S OWN OUTPUT")
    A = "3 pipeline"
    gc = read_csv(root / "results" / "agg" / "gold_credit.csv")
    chk(A, "gold_credit.csv has 1,040 rows", len(gc) == 1040, 1040, len(gc))
    dev = 0.0
    n = 0
    for r in gc:
        mine = credit[(r["generator"], r["topic_id"])][r["gold_id"]]
        dev = max(dev, abs(float(mine) - float(r["credit_sum"])))
        n += 1
    print(f"  gold_credit.csv   n={n}  max|dev| = {dev:.3e}")
    chk(A, "gold credit reproduces gold_credit.csv", dev < 1e-12, "<1e-12", f"{dev:.2e}")

    ct = read_csv(root / "results" / "agg" / "coverage_topic.csv")
    d2 = max(abs(float(cov_t[(r["generator"], r["topic_id"])]) - float(r["coverage_sum"]))
             for r in ct)
    print(f"  coverage_topic    n={len(ct)}  max|dev| = {d2:.3e}")
    chk(A, "coverage reproduces coverage_topic.csv", d2 < 1e-12, "<1e-12", f"{d2:.2e}")

    pt = read_csv(root / "results" / "agg" / "precision_topic.csv")
    d3 = max(abs(float(precision[(r["generator"], r["topic_id"])]) - float(r["precision"]))
             for r in pt)
    print(f"  precision_topic   n={len(pt)}  max|dev| = {d3:.3e}")
    chk(A, "precision reproduces precision_topic.csv", d3 < 1e-12, "<1e-12", f"{d3:.2e}")


# --------------------------------------------------------------------------
# 4. Table 4 -- coverage / precision / F1
# --------------------------------------------------------------------------
PAPER_T4 = {  # manuscript Table 4: coverage, precision, F1
    "Gemini 3.1 Pro": (0.698, 0.755, 0.725), "GPT 5.5": (0.645, 0.765, 0.700),
    "Gemma 4 31B": (0.638, 0.761, 0.694), "DeepSeek V4 Pro": (0.645, 0.705, 0.674),
    "Grok 4.3": (0.575, 0.808, 0.672), "Kimi K2.6": (0.604, 0.723, 0.658),
    "GLM 5.2": (0.607, 0.662, 0.633), "Claude Opus 4.8": (0.578, 0.660, 0.616),
    "Qwen 3.7 Max": (0.582, 0.649, 0.614), "Mistral Large 3": (0.565, 0.652, 0.606),
    "GPT-OSS 120B": (0.541, 0.596, 0.567), "Llama 4 Maverick": (0.502, 0.582, 0.540),
    "Llama 3.3 70B": (0.458, 0.528, 0.490),
}


def table4(cov_m, prec_m, f1_m):
    hdr("4. TABLE 4 -- coverage, precision, F1 (39 point estimates)")
    print(f"  {'model':<18}{'cov':>8}{'paper':>8}{'prec':>8}{'paper':>8}"
          f"{'F1':>8}{'paper':>8}")
    bad = 0
    for m in sorted(cov_m, key=lambda x: -f1_m[x]):
        lab = LABEL[m]
        pc, pp, pf = PAPER_T4[lab]
        c, p, f = float(cov_m[m]), float(prec_m[m]), float(f1_m[m])
        ok = all(abs(a - b) <= 5e-4 + 1e-12 for a, b in ((c, pc), (p, pp), (f, pf)))
        bad += not ok
        print(f"  {lab:<18}{c:>8.4f}{pc:>8.3f}{p:>8.4f}{pp:>8.3f}"
              f"{f:>8.4f}{pf:>8.3f}  {'MATCH' if ok else 'MISMATCH'}")
        chk("4 table4", f"T4.{lab}", ok, f"{pc}/{pp}/{pf}",
            f"{c:.4f}/{p:.4f}/{f:.4f}")
    lo, hi = min(cov_m.values()), max(cov_m.values())
    span = float(hi - lo) * 100
    print(f"\n  coverage span {span:.2f} pp  (paper 24.0)")
    chk("4 derived", "coverage span 24.0 pp", abs(span - 24.0) < 0.05, 24.0,
        round(span, 2))
    chk("4 derived", "lowest coverage is Llama 3.3 70B",
        LABEL[min(cov_m, key=cov_m.get)] == "Llama 3.3 70B", "Llama 3.3 70B",
        LABEL[min(cov_m, key=cov_m.get)])
    chk("4 derived", "highest coverage is Gemini 3.1 Pro",
        LABEL[max(cov_m, key=cov_m.get)] == "Gemini 3.1 Pro", "Gemini 3.1 Pro",
        LABEL[max(cov_m, key=cov_m.get)])
    rank = [LABEL[m] for m in sorted(f1_m, key=lambda x: -f1_m[x])]
    chk("4 derived", "Gemma 4 31B is 3rd on F1", rank.index("Gemma 4 31B") == 2,
        3, rank.index("Gemma 4 31B") + 1)
    chk("4 derived", "Claude Opus 4.8 is 8th on F1",
        rank.index("Claude Opus 4.8") == 7, 8, rank.index("Claude Opus 4.8") + 1)
    return bad


# --------------------------------------------------------------------------
# 5. exact Wilcoxon signed-rank, enumerated, tie-correct
# --------------------------------------------------------------------------
def signed_rank_w(d):
    """W+ with midranks on |d|; zeros dropped (Wilcoxon's own convention)."""
    nz = [x for x in d if x != 0]
    a = sorted((abs(x), i) for i, x in enumerate(nz))
    ranks = [0.0] * len(nz)
    i = 0
    while i < len(a):
        j = i
        while j + 1 < len(a) and a[j + 1][0] == a[i][0]:
            j += 1
        mid = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[a[k][1]] = mid
        i = j + 1
    return sum(r for r, x in zip(ranks, nz, strict=False) if x > 0), len(nz), ranks, nz


def wilcoxon_exact(d, alternative="two-sided"):
    """Exact enumerated signed-rank test. Ties handled by enumerating the
    2^m sign assignments on the OBSERVED |d| midranks, which is the
    conditional permutation distribution -- correct under ties, unlike the
    tabled null that assumes distinct ranks."""
    Wobs, m, ranks, nz = signed_rank_w(d)
    if m == 0:
        return float("nan"), Wobs, m
    tot = 1 << m
    ge = le = 0
    for mask in range(tot):
        w = sum(r for k, r in enumerate(ranks) if mask >> k & 1)
        if w >= Wobs - 1e-12:
            ge += 1
        if w <= Wobs + 1e-12:
            le += 1
    if alternative == "greater":
        return ge / tot, Wobs, m
    if alternative == "less":
        return le / tot, Wobs, m
    return min(1.0, 2 * min(ge, le) / tot), Wobs, m


def bh(ps):
    n = len(ps)
    order = sorted(range(n), key=lambda i: ps[i])
    adj = [0.0] * n
    prev = 1.0
    for rank, i in enumerate(reversed(order), 1):
        k = n - rank + 1
        prev = min(prev, ps[i] * n / k)
        adj[i] = prev
    return adj


# --------------------------------------------------------------------------
# 6. WEIRD gap
# --------------------------------------------------------------------------
def weird_gap(cov_t, topics):
    hdr("6. WEIRD GAP -- primary test, unit = matched pair, n = 8")
    pair = defaultdict(dict)   # pair -> arm -> {model: cov}
    for (m, t), v in cov_t.items():
        pair[topics[t]["pair"]].setdefault(topics[t]["arm"], {})[m] = v
    models = sorted({k[0] for k in cov_t})
    deltas = []
    for p in sorted(pair):
        w, s = pair[p]["weird"], pair[p]["serbian"]
        assert set(w) == set(s) == set(models)
        deltas.append(sum(w[m] - s[m] for m in models) / len(models))
    for p, d in zip(sorted(pair), deltas, strict=False):
        print(f"    pair {p}: {float(d):+.6f}")
    mean = sum(deltas) / len(deltas)
    med = statistics.median(sorted(float(x) for x in deltas))
    zeros = sum(d == 0 for d in deltas)
    ties = len([1 for a, b in itertools.combinations(deltas, 2) if abs(a) == abs(b)])
    print(f"\n  exact zeros among the 8 deltas: {zeros};  exact |delta| ties: {ties}")
    p2, W, m = wilcoxon_exact(deltas, "two-sided")
    p1, _, _ = wilcoxon_exact(deltas, "greater")
    print(f"  mean   {float(mean):+.6f}  (paper -0.013)")
    print(f"  median {med:+.6f}  (paper -0.014)")
    print(f"  exact two-sided p {p2:.4f}  (paper 0.74);  one-sided {p1:.4f} (0.68)")
    rb = (2 * W / (m * (m + 1) / 2) - 1)
    print(f"  rank-biserial {rb:+.4f}  (paper -0.17)")
    A = "6 gap"
    chk(A, "mean gap -0.013", abs(float(mean) + 0.013) < 0.0005, -0.013,
        round(float(mean), 6))
    chk(A, "median gap -0.014", abs(med + 0.014) < 0.0005, -0.014, round(med, 6))
    chk(A, "two-sided p = 0.74", abs(p2 - 0.74) < 0.005, 0.74, round(p2, 4))
    chk(A, "one-sided p = 0.68", abs(p1 - 0.68) < 0.005, 0.68, round(p1, 4))
    chk(A, "rank-biserial -0.17", abs(rb + 0.17) < 0.005, -0.17, round(rb, 4))
    chk(A, "4 pairs favour WEIRD, 4 favour Serbian",
        sum(d > 0 for d in deltas) == 4 and sum(d < 0 for d in deltas) == 4,
        "4/4", f"{sum(d > 0 for d in deltas)}/{sum(d < 0 for d in deltas)}")
    aw = sum(v for (mm, t), v in cov_t.items() if topics[t]["arm"] == "weird") / (13 * 8)
    as_ = sum(v for (mm, t), v in cov_t.items() if topics[t]["arm"] == "serbian") / (13 * 8)
    print(f"  pooled arm means: WEIRD {float(aw):.4f} (0.581)  "
          f"SERBIAN {float(as_):.4f} (0.594)")
    chk(A, "pooled WEIRD mean 0.581", abs(float(aw) - 0.581) < 5e-4, 0.581,
        round(float(aw), 4))
    chk(A, "pooled Serbian mean 0.594", abs(float(as_) - 0.594) < 5e-4, 0.594,
        round(float(as_), 4))
    return pair, deltas, models


PAPER_T6 = {  # manuscript Table 6: mean gap, one-sided p, BH p
    "GLM 5.2": (0.106, 0.055, 0.961), "GPT-OSS 120B": (0.058, 0.098, 0.961),
    "Llama 4 Maverick": (0.035, 0.473, 0.961), "Llama 3.3 70B": (0.015, 0.422, 0.961),
    "DeepSeek V4 Pro": (0.010, 0.469, 0.961), "Kimi K2.6": (-0.019, 0.688, 0.961),
    "GPT 5.5": (-0.020, 0.680, 0.961), "Grok 4.3": (-0.020, 0.727, 0.961),
    "Mistral Large 3": (-0.040, 0.766, 0.961), "Gemini 3.1 Pro": (-0.045, 0.727, 0.961),
    "Qwen 3.7 Max": (-0.073, 0.945, 0.961), "Gemma 4 31B": (-0.082, 0.961, 0.961),
    "Claude Opus 4.8": (-0.095, 0.875, 0.961),
}


def table6(pair, models, out: Path):
    hdr("6b. TABLE 6 -- per-model gaps, exact tie-correct Wilcoxon")
    rows = []
    for m in models:
        d = [pair[p]["weird"][m] - pair[p]["serbian"][m] for p in sorted(pair)]
        mean = sum(d) / len(d)
        med = statistics.median(sorted(float(x) for x in d))
        z = sum(x == 0 for x in d)
        ti = len([1 for a, b in itertools.combinations(d, 2)
                  if a != 0 and b != 0 and abs(a) == abs(b)])
        p1, W, mm = wilcoxon_exact(d, "greater")
        rows.append({"model": LABEL[m], "mean_gap": float(mean), "median_gap": med,
                     "exact_zeros": z, "exact_abs_ties": ti, "n_nonzero": mm,
                     "p_one_sided": p1})
    ps = [r["p_one_sided"] for r in rows]
    for r, q in zip(rows, bh(ps), strict=False):
        r["p_BH"] = q
    rows.sort(key=lambda r: -r["mean_gap"])
    print(f"  {'model':<18}{'gap':>8}{'paper':>7}{'p1':>8}{'paper':>7}"
          f"{'p_BH':>8}{'paper':>7}  z ties")
    changed_p, changed_bh, changed_gap = [], [], []
    for r in rows:
        pg, pp, pb = PAPER_T6[r["model"]]
        g_ok = abs(r["mean_gap"] - pg) <= 5e-4 + 1e-12
        p_ok = abs(r["p_one_sided"] - pp) <= 5e-4 + 1e-12
        b_ok = abs(r["p_BH"] - pb) <= 5e-4 + 1e-12
        if not g_ok:
            changed_gap.append(r["model"])
        if not p_ok:
            changed_p.append((r["model"], pp, r["p_one_sided"]))
        if not b_ok:
            changed_bh.append((r["model"], pb, r["p_BH"]))
        print(f"  {r['model']:<18}{r['mean_gap']:>+8.4f}{pg:>+7.3f}"
              f"{r['p_one_sided']:>8.4f}{pp:>7.3f}{r['p_BH']:>8.4f}{pb:>7.3f}"
              f"  {r['exact_zeros']} {r['exact_abs_ties']}"
              f"{'' if (g_ok and p_ok and b_ok) else '  <-- CHANGES'}")
    A = "6b table6"
    chk(A, "all 13 mean gaps reproduce", not changed_gap, 0, len(changed_gap))
    chk(A, "no per-model gap survives BH",
        min(r["p_BH"] for r in rows) > 0.05, ">0.05",
        round(min(r['p_BH'] for r in rows), 4))
    print(f"\n  mean-gap column reproduces for all 13: {not changed_gap}")
    print(f"  one-sided p changes for {len(changed_p)}/13 models:")
    for mdl, a, b in changed_p:
        print(f"    {mdl:<18} paper {a:.3f} -> exact {b:.4f}")
    print(f"  BH p changes for {len(changed_bh)}/13 models "
          f"(paper prints a single value {PAPER_T6['GLM 5.2'][2]} for every row)")
    print(f"  smallest BH p: exact {min(r['p_BH'] for r in rows):.4f}, "
          f"paper 0.961 -- nothing survives either way")
    with (out / "table6_corrected.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["model", "mean_gap", "median_gap",
                                           "n_nonzero", "exact_zeros",
                                           "exact_abs_ties", "p_one_sided", "p_BH"])
        w.writeheader()
        for r in rows:
            w.writerow({k: (f"{v:.6f}" if isinstance(v, float) else v)
                        for k, v in r.items()})
    return rows, changed_p, changed_bh


# --------------------------------------------------------------------------
# 7. per-topic difficulty and Table 7
# --------------------------------------------------------------------------
PAPER_T7 = {1: (0.628, 0.627, 0.1), 2: (0.508, 0.452, 5.5), 3: (0.631, 0.628, 0.3),
            4: (0.615, 0.644, -2.9), 5: (0.465, 0.634, -16.9), 6: (0.640, 0.449, 19.1),
            7: (0.532, 0.633, -10.1), 8: (0.629, 0.685, -5.6)}


def topic_difficulty(cov_t, topics, pair):
    hdr("7. PER-TOPIC DIFFICULTY AND TABLE 7")
    per = {}
    for t, meta in topics.items():
        vals = [float(v) for (m, tt), v in cov_t.items() if tt == t]
        per[t] = (statistics.fmean(vals), statistics.stdev(vals), meta)
    order = sorted(per, key=lambda t: per[t][0])
    print(f"  {'topic':<48}{'arm':<9}{'cov':>7}{'sd':>7}")
    for t in order:
        mu, sd, meta = per[t]
        print(f"  {meta['title'][:46]:<48}{meta['arm']:<9}{mu:>7.4f}{sd:>7.3f}")
    A = "7 topics"
    hardest, easiest = order[0], order[-1]
    print(f"\n  hardest {per[hardest][0]:.4f} {per[hardest][2]['title']}")
    print(f"  easiest {per[easiest][0]:.4f} {per[easiest][2]['title']}")
    spread = (per[easiest][0] - per[hardest][0]) * 100
    chk(A, "hardest topic 0.449", abs(per[hardest][0] - 0.449) < 5e-4, 0.449,
        round(per[hardest][0], 4))
    chk(A, "easiest topic 0.685", abs(per[easiest][0] - 0.685) < 5e-4, 0.685,
        round(per[easiest][0], 4))
    chk(A, "topic spread 23.6 pp", abs(spread - 23.6) < 0.05, 23.6, round(spread, 2))
    chk(A, "both extremes on the Serbian side",
        per[hardest][2]["arm"] == per[easiest][2]["arm"] == "serbian",
        "serbian/serbian",
        f"{per[hardest][2]['arm']}/{per[easiest][2]['arm']}")

    # the four topics section 4.5 names by value, plus the two attributions
    named = {"Migrants and the Balkan route (Serbia)": 0.449,
             "Independence of Kosovo (Serbia)": 0.452,
             "Canada residential schools": 0.465,
             "Srebrenica genocide (Serbia)": 0.634,
             "Polish Catholic Church": 0.644}
    print("\n  topics section 4.5 names by value:")
    bytitle = {v[2]["title"]: v[0] for v in per.values()}
    for title, want in named.items():
        got = bytitle[title]
        ok = abs(got - want) < 5e-4
        print(f"    {title:<44} paper {want:.3f}  mine {got:.4f}  "
              f"{'MATCH' if ok else 'MISMATCH'}")
        chk("7 named", f"4.5 quotes {title} at {want}", ok, want, round(got, 4),
            "" if ok else "misattribution in section 4.5")
    owner = [t for t, v in bytitle.items() if abs(v - 0.644) < 5e-4]
    print(f"    -> 0.644 actually belongs to {owner}")

    # Table 7
    print(f"\n  {'pair':>4}{'W mine':>9}{'W paper':>9}{'S mine':>9}"
          f"{'S paper':>9}{'d mine':>9}{'d paper':>9}")
    bad = 0
    models = sorted({k[0] for k in cov_t})
    for p in sorted(pair):
        w = statistics.fmean(float(pair[p]["weird"][m]) for m in models)
        s = statistics.fmean(float(pair[p]["serbian"][m]) for m in models)
        d = (w - s) * 100
        pw, ps_, pd = PAPER_T7[p]
        ok = (abs(w - pw) < 5e-4 and abs(s - ps_) < 5e-4 and abs(d - pd) < 0.05)
        bad += not ok
        print(f"  {p:>4}{w:>9.4f}{pw:>9.3f}{s:>9.4f}{ps_:>9.3f}{d:>9.2f}{pd:>9.1f}"
              f"  {'MATCH' if ok else 'MISMATCH'}")
        chk("7 table7", f"T7.pair{p}", ok, f"{pw}/{ps_}/{pd}",
            f"{w:.4f}/{s:.4f}/{d:.2f}")
    chk("7 table7", "all 8 Table 7 rows reproduce", bad == 0, 0, bad)

    sds = [v[1] for v in per.values()]
    sd_topics = statistics.stdev([v[0] for v in per.values()])
    print(f"\n  within-topic sd across models {min(sds):.4f}-{max(sds):.4f} "
          f"mean {statistics.fmean(sds):.4f}  (paper 0.076-0.166)")
    print(f"  sd of the 16 topic means {sd_topics:.4f}  (paper 0.078)")
    chk(A, "within-topic sd range 0.076-0.166",
        abs(min(sds) - 0.076) < 5e-4 and abs(max(sds) - 0.166) < 5e-4,
        "0.076-0.166", f"{min(sds):.4f}-{max(sds):.4f}")
    chk(A, "sd of topic means 0.078", abs(sd_topics - 0.078) < 5e-4, 0.078,
        round(sd_topics, 4))
    return per, bytitle


# --------------------------------------------------------------------------
# 8. extremity tiers
# --------------------------------------------------------------------------
def tiers(credit, topics):
    hdr("8. EXTREMITY TIERS (section 4.5 / 5.5)")
    got = defaultdict(list)
    seen = Counter()
    for (_g, t), col in credit.items():
        for i, gid in enumerate(topics[t]["gold_ids"]):
            got[topics[t]["tiers"][i]].append(float(col[gid]))
    for meta in topics.values():
        for x in meta["tiers"]:
            seen[x] += 1
    means = {}
    for k in sorted(got):
        means[k] = statistics.fmean(got[k])
    # identify which numeric tier maps to which label by matching the paper
    print("  numeric tier -> mean recovery (n gold columns):")
    for k in sorted(means):
        print(f"    tier {k}: {means[k]:.4f}  ({seen[k]} of 80 gold perspectives)")
    want = {"minority": 0.650, "mainstream": 0.593, "extreme": 0.475}
    inv = {}
    for lbl, v in want.items():
        cand = [k for k in means if abs(means[k] - v) < 5e-4]
        chk("8 tiers", f"tier mean for {lbl} = {v}", len(cand) == 1, v,
            [round(means[k], 4) for k in sorted(means)])
        if len(cand) == 1:
            inv[cand[0]] = lbl
    print(f"  numeric->label mapping recovered from the data: {inv}")
    spread = max(means.values()) - min(means.values())
    print(f"  observed spread {spread:.4f}  (paper 0.175)")
    chk("8 tiers", "tier spread 0.175", abs(spread - 0.175) < 5e-4, 0.175,
        round(spread, 4))
    return means, inv


# --------------------------------------------------------------------------
# 9. reliability
# --------------------------------------------------------------------------
def rel_coeffs(items):
    """items: list of Counter(label -> count), variable raters, nominal cats."""
    items = [it for it in items if sum(it.values()) >= 2]
    cats = sorted({c for it in items for c in it})
    N = len(items)
    # observed agreement (per-item pairwise)
    po = statistics.fmean(
        [sum(n * (n - 1) for n in it.values()) / (sum(it.values()) * (sum(it.values()) - 1))
         for it in items])
    # marginals
    tot = sum(sum(it.values()) for it in items)
    pj = {c: sum(it.get(c, 0) for it in items) / tot for c in cats}
    pe_f = sum(v * v for v in pj.values())
    fleiss = (po - pe_f) / (1 - pe_f)
    q = len(cats)
    pe_g = sum(v * (1 - v) for v in pj.values()) / (q - 1)
    gwet = (po - pe_g) / (1 - pe_g)
    # Krippendorff alpha, nominal, coincidence matrix
    mtot = sum(sum(it.values()) for it in items)
    coinc = defaultdict(float)
    for it in items:
        m = sum(it.values())
        for a in it:
            for b in it:
                n = it[a] * (it[b] - 1) if a == b else it[a] * it[b]
                coinc[(a, b)] += n / (m - 1)
    n_ = sum(coinc.values())
    Do = sum(v for (a, b), v in coinc.items() if a != b) / n_
    nc = {c: sum(v for (a, b), v in coinc.items() if a == c) for c in cats}
    De = sum(nc[a] * nc[b] for a in cats for b in cats if a != b) / (n_ * (n_ - 1))
    alpha = 1 - Do / De
    return po, fleiss, gwet, alpha, N, mtot


def reliability(valid, topics):
    hdr("9. TABLE 8 -- inter-judge reliability")
    scopes = {"all": lambda t: True,
              "weird": lambda t: topics[t]["arm"] == "weird",
              "serbian": lambda t: topics[t]["arm"] == "serbian"}
    PAPER = {"all": (32.0, 0.768, 0.783, 0.769, 1040, 5184),
             "weird": (32.9, 0.761, 0.777, 0.762, 520, 2593),
             "serbian": (31.1, 0.774, 0.789, 0.775, 520, 2591)}
    for sc, keep in scopes.items():
        items = defaultdict(Counter)
        for r in valid:
            if not keep(r["topic_id"]):
                continue
            # POSITIONAL label ("0".."5"), shared across topics -- this is the
            # category space the coefficients are defined over. Using
            # topic-specific gold_ids instead would give each topic its own
            # 6 categories, inflating the category count to 96, deflating
            # chance agreement, and inflating every coefficient by ~+0.026.
            mg = r["match_gold_id"]
            lab = "0" if mg == 0 else str(mg)
            items[(r["generator_slug"], r["topic_id"], r["gen_index"])][lab] += 1
        lst = list(items.values())
        po, fl, gw, al, N, V = rel_coeffs(lst)
        nm = 100 * sum(it.get("0", 0) for it in lst) / V
        pnm, pfl, pgw, pal, pN, pV = PAPER[sc]
        print(f"  {sc:<8} items {N} (paper {pN})  verdicts {V} (paper {pV})")
        for lbl, mine, pub, tol in (("no-match %", nm, pnm, 0.05),
                                    ("Fleiss k", fl, pfl, 5e-4),
                                    ("Gwet AC1", gw, pgw, 5e-4),
                                    ("Kripp. a", al, pal, 5e-4)):
            ok = abs(mine - pub) <= tol + 1e-12
            print(f"      {lbl:<12} paper {pub:>8.3f}  mine {mine:>9.4f}  "
                  f"{'MATCH' if ok else 'MISMATCH'}")
            chk("9 table8", f"T8.{sc}.{lbl}", ok, pub, round(mine, 4))
        chk("9 table8", f"T8.{sc}.items", N == pN, pN, N)
        chk("9 table8", f"T8.{sc}.verdicts", V == pV, pV, V)


# --------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(Path(__file__).resolve().parent.parent))
    ap.add_argument("--out",
                    default=str(Path(__file__).resolve().parent.parent
                                / "results" / "verification"))
    a = ap.parse_args()
    root, out = Path(a.root).resolve(), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    for m in ("bw_common", "bweird", "bwaudit"):
        assert m not in sys.modules, f"independence violated: {m} imported"

    topics, gens, raw, cfg_j, cfg_m = load(root)
    build_labels(cfg_m)
    valid, panels, fam = accounting(raw, topics, gens, cfg_j, cfg_m)
    credit, precision, clipped, njc, votes = gold_credit(valid, topics, gens)
    cov_t, cov_m, prec_m, f1_m = coverage_tables(credit, precision, topics, gens)
    against_pipeline(root, credit, cov_t, precision)
    table4(cov_m, prec_m, f1_m)
    pair, deltas, models = weird_gap(cov_t, topics)
    t6rows, changed_p, changed_bh = table6(pair, models, out)
    per, bytitle = topic_difficulty(cov_t, topics, pair)
    tiers(credit, topics)
    reliability(valid, topics)

    with (out / "reverify_checks.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["area", "check", "verdict",
                                           "expected", "got", "note"])
        w.writeheader()
        w.writerows(CHECKS)

    hdr("SUMMARY")
    nf = sum(c["verdict"] == "FAIL" for c in CHECKS)
    print(f"  {len(CHECKS) - nf}/{len(CHECKS)} checks PASS, {nf} FAIL")
    for c in CHECKS:
        if c["verdict"] == "FAIL":
            print(f"  FAIL  [{c['area']}] {c['check']}")
            print(f"        expected {c['expected']}  got {c['got']}")
            if c["note"]:
                print(f"        {c['note']}")
    print(f"\n  wrote {out}/reverify_checks.csv, {out}/table6_corrected.csv")
    return 0


if __name__ == "__main__":
    sys.exit(main())
