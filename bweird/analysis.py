"""Analysis core for the Beyond WEIRD evaluation stages.

This is THE live implementation of the coverage rule. Stages 3-6 import it;
every number in ``results/agg/`` comes from here. Implements the
split-then-average aggregation scheme from the Methodology (Aggregation
section) plus the agreement, bootstrap and multiple-comparison primitives the
stages share.

INPUT DATA CONTRACT
-------------------
1. verdicts.jsonl — one JSON object per (judge x generation) verdict:
     {
       "generator":     "claude-opus-4.8",
       "topic_id":      "kosovo",
       "generation_id": "gen_003",          # stable within (generator, topic)
       "judge":         "gpt-5.5",
       "match":         "kos_p2",           # canonical gold perspective_id,
                                            # or null / "" / "0" for no-match
       "status":        "ok"                # "ok" | "error" | "abstain"
     }
   IMPORTANT: `match` must be the CANONICAL gold perspective_id. The judge
   prompt randomises gold order per judge, so positional outputs must be
   de-randomised back to canonical ids BEFORE this stage.

2. topics.json:
     {"topics": [
        {"topic_id": "kosovo", "pair_id": "secession", "arm": "serbian",
         "gold_ids": ["kos_p1", ..., "kos_p5"]},
        ...]}
   `arm` is "weird" or "serbian"; every pair_id must have exactly one of each.

3. panels.json:
     {"families":      {"claude-opus-4.8": "anthropic", ...},   # generators AND judges
      "base_panel":    ["gemini-3.1-pro", "gpt-5.5", ...],      # 5 judges
      "substitutions": {"anthropic": "qwen-3.7-max", ...}}      # family -> substitute judge
   Substitutes must come from families NOT already on the base panel,
   otherwise the resolved panel would contain a judge twice; this is
   validated and raises an error.

AGGREGATION (split-then-average)
--------------------------------
For one (generator, topic): a table with one row per generated perspective
and one column per gold perspective, one copy per judge. A judge's match
contributes one unit of credit to its cell; if a judge matched k generations
to the SAME gold, each gets 1/k, so each judge credits a gold at most once.
The panel table is the cell-wise average over judges, with per-generation
denominators: a judge that errored/abstained on a generation is dropped from
that generation's cells only.

Gold credit is the COLUMN SUM of the merged table (clipped to 1.0, which can
only trigger under partial abstention), read as the share of judges who found
that gold covered by any generation. The column MAX is also computed, because
the manuscript's Recall section currently describes a max rule — the two
differ whenever judges agree a gold is covered but disagree on which
generation covers it. Default downstream is the sum; see README.

Validity (precision input) per generation is the RAW share of ok judges that
assigned it to any gold (no split), per the manuscript's Precision section.
"""
from __future__ import annotations

import json
import logging
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

from bweird.config import JudgeConfig, ModelSpec
from bweird.errors import DataError

log = logging.getLogger("bw_eval")

NO_MATCH = "0"  # canonical no-match label used in agreement analyses

# Repo-root-relative defaults for stages 3-6, resolved from this file so each
# stage runs from any working directory; every path is still overridable on
# the stage's own command line.
ROOT_DIR = Path(__file__).resolve().parent.parent
ADAPTED_DIR = ROOT_DIR / "results" / "adapted"
AGG_DIR = ROOT_DIR / "results" / "agg"

# ---------------------------------------------------------------------------
# Loading & validation
# ---------------------------------------------------------------------------

def load_eval_topics(path: str | Path) -> dict:
    """Load the eval-contract topics.json.

    Enforces unique ids and one arm of each per pair. Distinct from
    :func:`bweird.schemas.load_topics`, which parses the
    study's canonical topic instrument (a bare list) into typed ``Topic``
    objects; this loads the adapter-produced ``{"topics": [...]}`` file that
    stages 3-6 consume.
    """
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    topics = {}
    for t in data["topics"]:
        tid = t["topic_id"]
        if tid in topics:
            raise DataError(f"duplicate topic_id {tid}")
        if t["arm"] not in ("weird", "serbian"):
            raise DataError(f"topic {tid}: arm must be 'weird' or 'serbian'")
        if len(t["gold_ids"]) != len(set(t["gold_ids"])):
            raise DataError(f"topic {tid}: duplicate gold_ids")
        topics[tid] = t
    # every pair must have exactly one weird and one serbian arm
    pairs = {}
    for t in topics.values():
        pairs.setdefault(t["pair_id"], []).append(t["arm"])
    for pid, arms in pairs.items():
        if sorted(arms) != ["serbian", "weird"]:
            log.warning("pair %s does not have exactly one weird and one serbian arm: %s",
                        pid, arms)
    return topics


def load_panels(path: str | Path) -> dict:
    """Load panels.json, checking every base judge has a family label."""
    p = json.loads(Path(path).read_text(encoding="utf-8"))
    for key in ("families", "base_panel", "substitutions"):
        if key not in p:
            raise DataError(f"panels.json missing '{key}'")
    for j in p["base_panel"]:
        if j not in p["families"]:
            raise DataError(f"base panel judge {j} missing from families map")
    return p


def _norm_match(v) -> str | None:
    """Normalise a raw match value to canonical gold_id string or None (no-match)."""
    if v is None:
        return None
    s = str(v).strip()
    if s in ("", "0", "null", "None", "no_match", "nomatch"):
        return None
    return s


def load_verdicts(path: str | Path, topics: dict) -> pd.DataFrame:
    """Load verdicts.jsonl into a frame, validating gold ids and de-duplicating.

    Out-of-topic gold ids are demoted to no-match and duplicated
    (generator, topic, generation, judge) tuples keep the LAST record, which is
    how ``--retry-abstentions`` reruns supersede the abstentions they replace.
    """
    rows = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            rows.append({
                "generator": r["generator"],
                "topic_id": r["topic_id"],
                "generation_id": str(r["generation_id"]),
                "judge": r["judge"],
                "match": _norm_match(r.get("match")),
                "status": r.get("status", "ok"),
            })
    df = pd.DataFrame(rows)
    if df.empty:
        raise DataError("no verdicts loaded")
    # validate topic ids and gold ids
    unknown_topics = set(df.topic_id) - set(topics)
    if unknown_topics:
        raise DataError(f"verdicts reference unknown topics: {sorted(unknown_topics)}")
    bad = 0
    for tid, sub in df[df.match.notna()].groupby("topic_id"):
        gold = set(topics[tid]["gold_ids"])
        mask = ~sub.match.isin(gold)
        if mask.any():
            bad += int(mask.sum())
            df.loc[sub.index[mask], "match"] = None
    if bad:
        log.warning("%d verdicts referenced gold ids not in their topic; treated as no-match", bad)
    dup = df.duplicated(subset=["generator", "topic_id", "generation_id", "judge"])
    if dup.any():
        log.warning("%d duplicate (generator,topic,generation,judge) verdicts; keeping last",
                    int(dup.sum()))
        df = df[~df.duplicated(subset=["generator", "topic_id", "generation_id", "judge"],
                               keep="last")]
    return df


# ---------------------------------------------------------------------------
# Panel resolution
# ---------------------------------------------------------------------------

def _judge_config_from_panels_dict(panels: dict) -> JudgeConfig:
    """Adapt the eval-contract panels.json dict into a typed JudgeConfig.

    Reuses bweird.config's family-disjoint substitution algorithm instead of
    re-deriving it here (this used to be a second, independently-maintained
    implementation of the same rule).
    """
    families = panels["families"]
    base = tuple(ModelSpec(slug=j, family=families[j].lower(), display_name=j)
                 for j in panels["base_panel"])
    substitutes = {
        fam.lower(): ModelSpec(slug=slug, family=families[slug].lower(), display_name=slug)
        for fam, slug in panels["substitutions"].items()
    }
    return JudgeConfig(base_panel=base, substitutes=substitutes)


def resolve_panel(generator: str, panels: dict, config: str = "disjoint") -> list[str]:
    """Return the 5-judge panel for a generator.

    config='disjoint' applies the family-disjointness rule with substitution
    (Table 3); config='full' returns the base panel unchanged (used only by
    the bias-control analysis).
    """
    fam = panels["families"].get(generator)
    if fam is None:
        raise DataError(f"generator {generator} missing from families map")

    base = list(panels["base_panel"])
    if config == "full":
        _check_distinct_families(base, panels, f"generator {generator} (full panel)")
        return base

    judge_config = _judge_config_from_panels_dict(panels)
    panel = judge_config.build_panel(fam)
    return [member.judge.slug for member in panel]


def _check_distinct_families(panel_list: list[str], panels: dict, context: str):
    """Validate pairwise-distinct families for the (unsubstituted) 'full' panel.

    The 'disjoint' path's equivalent validation is handled by
    JudgeConfig.build_panel; this remains only for 'full' mode, which
    deliberately skips substitution so build_panel doesn't apply.
    """
    fams = [panels["families"][j] for j in panel_list]
    dupes = sorted({f for f in fams if fams.count(f) > 1})
    if dupes:
        raise DataError(
            f"panel for {context} contains two judges from the same family "
            f"{dupes}: {panel_list}. The panel must comprise five judges from "
            f"pairwise-distinct families; substitutes must come from families "
            f"not already represented on the panel.")


# ---------------------------------------------------------------------------
# Aggregation core (split-then-average)
# ---------------------------------------------------------------------------

def aggregate_model_topic(vdf: pd.DataFrame, gold_ids: list[str], panel: list[str]):
    """Aggregate one (generator, topic).

    vdf: verdict rows for this generator+topic (any judges; filtered to `panel`).
    Returns dict with:
      cells      DataFrame [generation_id, gold_id, weight, n_judges]
      gold       DataFrame [gold_id, credit_sum, credit_max]
      validity   DataFrame [generation_id, validity, n_judges]
      coverage_sum, coverage_max  floats (mean credit over gold_ids)
      n_generations
    """
    vdf = vdf[vdf.judge.isin(panel)]
    ok = vdf[vdf.status == "ok"]

    # per-judge vote dict: generation_id -> gold_id or None
    # (pd.isna guard: pandas >=3.0 stores None as NaN in string columns)
    votes = {j: {gid: (None if pd.isna(m) else m)
                 for gid, m in zip(g.generation_id, g.match, strict=False)}
             for j, g in ok.groupby("judge")}

    gens = sorted(vdf.generation_id.unique())
    if not gens:
        raise ValueError("no generations for this (generator, topic)")

    # split credits within each judge: 1/k when a judge matched k generations
    # to the same gold (k computed over the generations that judge actually judged)
    credit = {}  # (judge, gen, gold) -> float
    for j, jv in votes.items():
        k = Counter(m for m in jv.values() if m is not None)
        for gen, m in jv.items():
            if m is not None:
                credit[(j, gen, m)] = 1.0 / k[m]

    cell_rows, val_rows = [], []
    for gen in gens:
        ok_judges = [j for j in panel if gen in votes.get(j, {})]
        n = len(ok_judges)
        if n == 0:
            log.warning("generation %s has zero valid judge verdicts; excluded", gen)
            continue
        matched = sum(1 for j in ok_judges if votes[j][gen] is not None)
        val_rows.append((gen, matched / n, n))
        for c in gold_ids:
            w = sum(credit.get((j, gen, c), 0.0) for j in ok_judges) / n
            cell_rows.append((gen, c, w, n))

    cells = pd.DataFrame(cell_rows,
                         columns=["generation_id", "gold_id", "weight", "n_judges"])
    validity = pd.DataFrame(val_rows,
                            columns=["generation_id", "validity", "n_judges"])

    col_sum = (cells.groupby("gold_id").weight.sum()
               .reindex(gold_ids, fill_value=0.0))
    clipped = col_sum.clip(upper=1.0)
    if (col_sum > 1.0 + 1e-9).any():
        over = col_sum[col_sum > 1.0 + 1e-9]
        log.info("column sum >1 clipped for gold(s) %s (partial-abstention corner case)",
                 list(over.index))
    col_max = (cells.groupby("gold_id").weight.max()
               .reindex(gold_ids, fill_value=0.0))

    gold = pd.DataFrame({"gold_id": gold_ids,
                         "credit_sum": clipped.values,
                         "credit_max": col_max.values})
    return {
        "cells": cells,
        "gold": gold,
        "validity": validity,
        "coverage_sum": float(gold.credit_sum.mean()),
        "coverage_max": float(gold.credit_max.mean()),
        "n_generations": len(validity),
    }


def aggregate_all(verdicts: pd.DataFrame, topics: dict, panels: dict,
                  config: str = "disjoint",
                  generators: list[str] | None = None) -> dict[str, pd.DataFrame]:
    """Run aggregation for every (generator, topic) present in the verdicts.

    Returns dict of tidy DataFrames: cells, gold_credit, coverage_topic,
    validity, precision_topic.
    """
    gens_all = generators or sorted(verdicts.generator.unique())
    cells, gold_credit, cov_rows, val_rows, prec_rows = [], [], [], [], []
    for gmodel in gens_all:
        panel = resolve_panel(gmodel, panels, config)
        gdf = verdicts[verdicts.generator == gmodel]
        for tid, tdf in gdf.groupby("topic_id"):
            res = aggregate_model_topic(tdf, topics[tid]["gold_ids"], panel)
            c = res["cells"].copy()
            c.insert(0, "topic_id", tid)
            c.insert(0, "generator", gmodel)
            cells.append(c)
            g = res["gold"].copy()
            g.insert(0, "topic_id", tid)
            g.insert(0, "generator", gmodel)
            gold_credit.append(g)
            v = res["validity"].copy()
            v.insert(0, "topic_id", tid)
            v.insert(0, "generator", gmodel)
            val_rows.append(v)
            cov_rows.append((gmodel, tid, res["coverage_sum"], res["coverage_max"],
                             len(topics[tid]["gold_ids"])))
            prec_rows.append((gmodel, tid, float(res["validity"].validity.mean()),
                              res["n_generations"]))
    return {
        "cells": pd.concat(cells, ignore_index=True),
        "gold_credit": pd.concat(gold_credit, ignore_index=True),
        "coverage_topic": pd.DataFrame(
            cov_rows, columns=["generator", "topic_id", "coverage_sum",
                               "coverage_max", "n_golds"]),
        "validity": pd.concat(val_rows, ignore_index=True),
        "precision_topic": pd.DataFrame(
            prec_rows, columns=["generator", "topic_id", "precision",
                                "n_generations"]),
    }


# ---------------------------------------------------------------------------
# Agreement metrics (variable raters per item; nominal categories)
# ---------------------------------------------------------------------------
# items: list of Counter(label -> count). Items with <2 ratings are dropped.
#
# These stay hand-rolled rather than delegating to statsmodels/krippendorff:
# (1) fleiss_kappa needs the variable-rater generalisation -- statsmodels'
#     version asserts a fixed rater count per item, which real verdicts don't
#     have (an errored/abstained judge is simply absent from that item); (2)
# even where a library gives a mathematically-equivalent result, its
# different summation order changes the last bit of the float, which would
# "dirty" the committed results/agg/*.csv on every re-run -- verified
# empirically when trying the swap. This project treats that reproducibility
# as load-bearing (see the mixed-effects rounding note in 6_eval_stats.py).

def _prep_items(items):
    items = [it for it in items if sum(it.values()) >= 2]
    cats = sorted({c for it in items for c in it})
    return items, cats


def observed_agreement(items) -> float:
    """Mean pairwise agreement over items, each a {category: rater_count} dict."""
    items, _ = _prep_items(items)
    pa = []
    for it in items:
        n = sum(it.values())
        pa.append(sum(c * (c - 1) for c in it.values()) / (n * (n - 1)))
    return float(np.mean(pa))


def fleiss_kappa(items) -> float:
    """Fleiss' kappa. Deflates under a skewed no-match marginal; see gwet_ac1."""
    items, cats = _prep_items(items)
    pa = observed_agreement(items)
    total = sum(sum(it.values()) for it in items)
    pk = {c: sum(it.get(c, 0) for it in items) / total for c in cats}
    pe = sum(p * p for p in pk.values())
    return (pa - pe) / (1 - pe) if pe < 1 else float("nan")


def gwet_ac1(items) -> float:
    """Gwet's AC1: the kappa-paradox-robust counterpart to fleiss_kappa."""
    items, cats = _prep_items(items)
    pa = observed_agreement(items)
    n_cats = len(cats)
    if n_cats < 2:
        return float("nan")
    # pi_k: mean over items of the within-item proportion in category k
    pik = {c: float(np.mean([it.get(c, 0) / sum(it.values()) for it in items]))
           for c in cats}
    pe = sum(p * (1 - p) for p in pik.values()) / (n_cats - 1)
    return (pa - pe) / (1 - pe) if pe < 1 else float("nan")


def krippendorff_alpha(items) -> float:
    """Nominal-data alpha via the coincidence matrix; handles variable raters."""
    items, cats = _prep_items(items)
    idx = {c: i for i, c in enumerate(cats)}
    n_cats = len(cats)
    o = np.zeros((n_cats, n_cats))
    for it in items:
        n = sum(it.values())
        for c, nc in it.items():
            for k, nk in it.items():
                pairs = nc * (nk - 1) if c == k else nc * nk
                o[idx[c], idx[k]] += pairs / (n - 1)
    n_tot = o.sum()
    nc = o.sum(axis=1)
    d_obs = n_tot - np.trace(o)                       # observed disagreements
    d_exp = (n_tot * n_tot - (nc * nc).sum()) / max(n_tot - 1, 1)  # expected
    if d_exp == 0:
        return float("nan")
    return float(1 - d_obs / d_exp)


def cohen_kappa(a: list, b: list) -> float:
    """Cohen's kappa between two raters over their co-rated items."""
    assert len(a) == len(b)
    n = len(a)
    if n == 0:
        return float("nan")
    cats = sorted(set(a) | set(b))
    pa = sum(x == y for x, y in zip(a, b, strict=False)) / n
    fa, fb = Counter(a), Counter(b)
    pe = sum((fa[c] / n) * (fb[c] / n) for c in cats)
    return (pa - pe) / (1 - pe) if pe < 1 else float("nan")


# ---------------------------------------------------------------------------
# Plurality verdicts & bootstrap
# ---------------------------------------------------------------------------

def plurality_verdict(labels: list[str | None]) -> tuple[str, float]:
    """Most common label among a panel's verdicts, and the share supporting it.

    Ties break conservatively toward no-match; ties among golds only break
    to the lexicographically smallest id (deterministic; logged upstream).
    """
    lab = [NO_MATCH if x is None else x for x in labels]
    cnt = Counter(lab)
    top = max(cnt.values())
    tied = sorted(k for k, v in cnt.items() if v == top)
    chosen = NO_MATCH if NO_MATCH in tied else tied[0]
    return chosen, cnt[chosen] / len(lab)


def bootstrap_ci(values_by_unit: pd.Series, stat=np.mean, n_boot=10000,
                 seed=42, alpha=0.05):
    """Percentile bootstrap CI resampling the index units (e.g. topics)."""
    rng = np.random.default_rng(seed)
    vals = values_by_unit.to_numpy(dtype=float)
    n = len(vals)
    if n == 0:
        return float("nan"), float("nan"), float("nan")
    idx = rng.integers(0, n, size=(n_boot, n))
    boots = stat(vals[idx], axis=1)
    lo, hi = np.percentile(boots, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return float(stat(vals)), float(lo), float(hi)


def bh_correction(pvals: list[float]) -> list[float]:
    """Benjamini–Hochberg adjusted p-values."""
    p = np.asarray(pvals, dtype=float)
    m = len(p)
    order = np.argsort(p)
    adj = np.empty(m)
    running = 1.0
    for rank in range(m - 1, -1, -1):
        i = order[rank]
        running = min(running, p[i] * m / (rank + 1))
        adj[i] = running
    return adj.tolist()
