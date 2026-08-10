"""bw_common.py — shared loading, joining, and aggregation for the Beyond WEIRD analysis pack.

USAGE (run from the repository root)
  1) python reanalysis/bw_common.py --inspect   # verify schema + topic/pair/arm mapping
  2) Run the other scripts, or `make reanalysis` (see README.md for order).

All other scripts import this module. Run every command from the repo root. Nothing here mutates your data files.
"""

from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

# Repository root, resolved from this file's location so the pack runs from any
# working directory and on any machine.
ROOT = Path(__file__).resolve().parent.parent

# ----------------------------------------------------------------------------
# CONFIG
# ----------------------------------------------------------------------------
CONFIG = {
    # Paths are repo-root-relative; override on the command line if your data
    # lives elsewhere.
    "judgments_path": str(ROOT / "data" / "outputs" / "judgments.jsonl"),
    "generations_path": str(ROOT / "data" / "outputs" / "generations.jsonl"),
    "gold_path": str(ROOT / "data" / "gold_standard.json"),
    "out_dir": str(ROOT / "results" / "reanalysis"),

    # Column names in your files. Leave a value as None to auto-detect
    # (candidates listed further down). Set explicitly if --inspect guesses wrong.
    "fields": {
        # judgments.jsonl
        "j_generator": None,   # generator model name
        "j_topic": None,       # topic id/title
        "j_gen_index": None,   # index of the generated perspective (1-based in your file)
        "j_judge": None,       # judge model name
        "j_match": None,       # verdict: 0/no-match or gold index / gold perspective_id
        "j_error": None,       # optional error flag/message column
        "j_time": None,        # optional timestamp column (used for keep-most-recent dedup)
        # generations.jsonl
        "g_generator": None,
        "g_topic": None,
        "g_index": None,       # 0-based in your file
    },

    # Values of the match column that mean "no match".
    "no_match_values": {0, "0", "none", "no_match", "nomatch", "null", "NONE"},

    # Coverage rule: the credit-sum rule implemented in `panel_weights`, which
    # reproduces results/agg/gold_credit.csv to floating-point epsilon on all
    # 1,040 rows. `one_to_one_assign` implements the greedy one-to-one variant
    # that was tested and REJECTED (consistent ~2pp gap); it is kept only so the
    # comparison stays auditable. Not configurable — one rule, confirmed.

    # If gold_v2.json lacks pair/arm info, fill this after --inspect prints the topic ids:
    #   {"<topic_id>": {"pair": "pair01", "arm": "WEIRD"}, ...}
    "manual_topic_map": {},

    # Normalisation of arm labels found in gold_v2.json.
    "arm_normalize": {
        "weird": "WEIRD", "w": "WEIRD", "western": "WEIRD",
        "serbian": "SERBIAN", "s": "SERBIAN", "serbia": "SERBIAN",
        "balkan": "SERBIAN", "non-weird": "SERBIAN", "nonweird": "SERBIAN",
    },

    # Map raw model-name substrings -> published label, only needed if the
    # automatic normalised matching in published_label() fails (check --inspect).
    "published_aliases": {
        # "glm-5.1": "GLM 5.2",
    },

    # RNG seed for bootstraps.
    "seed": 20260722,
}

# Auto-detection candidates, tried in order.
_CANDIDATES = {
    "j_generator": ["generator_slug", "model_slug", "generator", "generator_model",
                    "gen_model", "model", "target_model"],
    "j_topic": ["topic_id", "topic", "topic_title", "topic_slug"],
    "j_gen_index": ["gen_index", "generation_index", "perspective_index", "gen_idx", "index"],
    "j_judge": ["judge_slug", "judge", "judge_model", "judge_name"],
    # match_gold_id is the already-de-randomized canonical slot (what we want).
    # match_presented is position in that judge's shuffled list and needs
    # presentation_order to decode — deliberately NOT a candidate here.
    "j_match": ["match_gold_id", "match", "verdict", "gold_index", "match_index",
                "gold_id", "matched_gold"],
    "j_error": ["error", "api_error", "error_message", "status", "failed"],
    "j_time": ["timestamp", "created_at", "time", "ts", "datetime"],
    "g_generator": ["model_slug", "generator_slug", "generator", "generator_model",
                    "gen_model", "model", "target_model"],
    "g_topic": ["topic_id", "topic", "topic_title", "topic_slug"],
    "g_index": ["index", "gen_index", "generation_index", "perspective_index", "gen_idx", "i"],
}

# Published results — full precision from results/agg/ranking.csv and
# weird_gap_summary.csv (confirmed byte-consistent with the manuscript's rounded
# Table 1 and Section 4.4 figures).
PUBLISHED_TABLE1 = {
    "Gemini 3.1 Pro":   {"coverage": 0.6975000, "precision": 0.7550000, "f1": 0.7251119},
    "GPT 5.5":          {"coverage": 0.6450000, "precision": 0.7650000, "f1": 0.6998936},
    "Gemma 4":          {"coverage": 0.6384375, "precision": 0.7612500, "f1": 0.6944558},
    "DeepSeek V4 Pro":  {"coverage": 0.6450000, "precision": 0.7050000, "f1": 0.6736667},
    "Grok 4.3":         {"coverage": 0.5750000, "precision": 0.8075000, "f1": 0.6716998},
    "Kimi K2.6":        {"coverage": 0.6043750, "precision": 0.7231250, "f1": 0.6584387},
    "GLM 5.2":          {"coverage": 0.6068750, "precision": 0.6618750, "f1": 0.6331829},
    "Claude Opus 4.8":  {"coverage": 0.5775000, "precision": 0.6600000, "f1": 0.6160000},
    "Qwen 3.7 Max":     {"coverage": 0.5815625, "precision": 0.6493750, "f1": 0.6136009},
    "Mistral Large 3":  {"coverage": 0.5650000, "precision": 0.6525000, "f1": 0.6056057},
    "GPT-OSS 120B":     {"coverage": 0.5412500, "precision": 0.5962500, "f1": 0.5674203},
    "Llama 4 Maverick": {"coverage": 0.5025000, "precision": 0.5825000, "f1": 0.5395507},
    "Llama 3.3 70B":    {"coverage": 0.4575000, "precision": 0.5275000, "f1": 0.4900127},
}
PUBLISHED_GAP = {"pooled_mean": -0.0130769, "pooled_median": -0.0140385,
                 "p_one_sided": 0.6796875, "p_two_sided": 0.7421875,
                 "rank_biserial": -0.1666667, "ci": (-0.0809615, 0.0582260)}
PUBLISHED_COUNTS = {"raw": 5228, "errors": 44, "duplicates": 28, "valid_reported": 5184}

# Authoritative slug -> published-label map, taken directly from ranking.csv's
# generator column (ground truth), not guessed by fuzzy matching. Extend this
# first if a new slug variant shows up; fuzzy matching is only the fallback.
_SLUG_TO_LABEL = {
    "google/gemini-3.1-pro-preview": "Gemini 3.1 Pro",
    "openai/gpt-5.5": "GPT 5.5",
    "google/gemma-4-31b-it": "Gemma 4",
    "deepseek/deepseek-v4-pro": "DeepSeek V4 Pro",
    "x-ai/grok-4.3": "Grok 4.3",
    "moonshotai/kimi-k2.6": "Kimi K2.6",
    "z-ai/glm-5.2": "GLM 5.2",
    "anthropic/claude-opus-4.8": "Claude Opus 4.8",
    "qwen/qwen3.7-max": "Qwen 3.7 Max",
    "mistralai/mistral-large-2512": "Mistral Large 3",
    "openai/gpt-oss-120b": "GPT-OSS 120B",
    "meta-llama/llama-4-maverick": "Llama 4 Maverick",
    "meta-llama/llama-3.3-70b-instruct": "Llama 3.3 70B",
    # judges, for completeness in --inspect output (not in PUBLISHED_TABLE1)
    "anthropic/claude-sonnet-5": "Claude Sonnet 5 (judge)",
}

# Family keywords for family-disjointness checks.
_FAMILY_KEYWORDS = [
    ("google", ["gemini", "gemma"]),
    ("openai", ["gpt", "o1", "o3", "oss"]),
    ("anthropic", ["claude"]),
    ("meta", ["llama"]),
    ("deepseek", ["deepseek"]),
    ("alibaba", ["qwen"]),
    ("moonshot", ["kimi"]),
    ("zai", ["glm"]),
    ("xai", ["grok"]),
    ("mistral", ["mistral", "ministral"]),
]


# ----------------------------------------------------------------------------
# Small helpers
# ----------------------------------------------------------------------------
def norm_name(s) -> str:
    """Lowercase, drop vendor prefix (before '/'), strip non-alphanumerics."""
    s = str(s)
    if "/" in s:
        s = s.split("/")[-1]
    return re.sub(r"[^a-z0-9]", "", s.lower())


def family_of(model_name) -> str:
    n = norm_name(model_name)
    for fam, kws in _FAMILY_KEYWORDS:
        if any(kw in n for kw in kws):
            # gpt-oss belongs to openai; ensure 'oss' alone doesn't misfire elsewhere
            if fam == "openai" and "oss" in n and "gpt" not in n:
                continue
            return fam
    return "unknown:" + n


def published_label(raw_model_name) -> str | None:
    """Map a raw model string from the data files to a PUBLISHED_TABLE1 key."""
    if raw_model_name in _SLUG_TO_LABEL:
        return _SLUG_TO_LABEL[raw_model_name]
    for pat, label in CONFIG["published_aliases"].items():
        if norm_name(pat) in norm_name(raw_model_name):
            return label
    n = norm_name(raw_model_name)
    best = None
    for label in PUBLISHED_TABLE1:
        p = norm_name(label)
        if p in n or n in p:
            if best is None or len(p) > len(norm_name(best)):
                best = label
    return best


def read_jsonl(path) -> pd.DataFrame:
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise SystemExit(f"{path}: bad JSON on line {i+1}: {e}") from e
    if not rows:
        raise SystemExit(f"{path}: empty file")
    return pd.DataFrame(rows)


def resolve_field(df: pd.DataFrame, key: str, required=True):
    explicit = CONFIG["fields"].get(key)
    if explicit:
        if explicit not in df.columns:
            raise SystemExit(f"CONFIG field {key}={explicit!r} not in columns {list(df.columns)}")
        return explicit
    for cand in _CANDIDATES[key]:
        if cand in df.columns:
            return cand
    if required:
        raise SystemExit(
            f"Could not auto-detect {key} among {list(df.columns)}.\n"
            f"Set CONFIG['fields'][{key!r}] in bw_common.py."
        )
    return None


def _outdir() -> Path:
    p = Path(CONFIG["out_dir"])
    p.mkdir(parents=True, exist_ok=True)
    return p


# ----------------------------------------------------------------------------
# Gold file: topic -> (pair, arm, ordered gold ids)
# ----------------------------------------------------------------------------
def load_gold() -> pd.DataFrame:
    """Return DataFrame [topic, pair, arm, gold_ids] with gold_ids an ordered list."""
    raw = json.loads(Path(CONFIG["gold_path"]).read_text(encoding="utf-8"))

    if isinstance(raw, dict):
        # either {"topics":[...]} or {topic_id: {...}}
        if "topics" in raw and isinstance(raw["topics"], list):
            items = raw["topics"]
        else:
            items = [{"__key": k, **v} if isinstance(v, dict) else {"__key": k, "value": v}
                     for k, v in raw.items()]
    elif isinstance(raw, list):
        items = raw
    else:
        raise SystemExit(f"{CONFIG['gold_path']}: unrecognised top-level JSON type {type(raw)}")

    def pick(d, keys):
        for k in keys:
            if k in d and d[k] is not None:
                return d[k]
        return None

    rows = []
    for it in items:
        if not isinstance(it, dict):
            continue
        topic = pick(it, ["topic_id", "topic", "id", "slug", "title", "topic_title", "__key"])
        pair = pick(it, ["pair", "pair_id", "pairid", "match_pair", "matched_pair"])
        arm = pick(it, ["arm", "culture", "context", "side", "weird", "group"])
        persp = pick(it, ["perspectives", "gold", "gold_perspectives", "golds"])
        gold_ids = []
        if isinstance(persp, list):
            for j, p in enumerate(persp):
                if isinstance(p, dict):
                    pid = pick(p, ["perspective_id", "id", "pid", "gold_id"])
                    gold_ids.append(pid if pid is not None else j + 1)
                else:
                    gold_ids.append(j + 1)
        if isinstance(arm, bool):  # e.g. "weird": true/false
            arm = "WEIRD" if arm else "SERBIAN"
        rows.append({"topic": topic, "pair": pair, "arm": arm, "gold_ids": gold_ids})

    g = pd.DataFrame(rows)
    if g.empty or g["topic"].isna().all():
        raise SystemExit(f"Could not parse topics out of {CONFIG['gold_path']}; run --inspect.")

    # Manual overrides / fill-ins.
    for t, meta in CONFIG["manual_topic_map"].items():
        m = g["topic"].astype(str) == str(t)
        if m.any():
            if "pair" in meta:
                g.loc[m, "pair"] = meta["pair"]
            if "arm" in meta:
                g.loc[m, "arm"] = meta["arm"]
        else:
            g = pd.concat([g, pd.DataFrame([{"topic": t, "pair": meta.get("pair"),
                                             "arm": meta.get("arm"), "gold_ids": []}])],
                          ignore_index=True)

    def norm_arm(a):
        if a is None or (isinstance(a, float) and np.isnan(a)):
            return None
        return CONFIG["arm_normalize"].get(str(a).strip().lower(), str(a).strip().upper())

    g["arm"] = g["arm"].map(norm_arm)
    return g


# ----------------------------------------------------------------------------
# Judgments: load, error-drop, dedup, canonicalise matches
# ----------------------------------------------------------------------------
def load_judgments(gold: pd.DataFrame | None = None):
    """Return (valid_df, counts, notes).

    valid_df columns: generator, topic, gen_index (as in file), judge, match_slot
    where match_slot is 0 (no match) or the canonical gold slot 1..5.
    """
    df = read_jsonl(CONFIG["judgments_path"])
    f = {k: resolve_field(df, k, required=(k in
         ("j_generator", "j_topic", "j_gen_index", "j_judge", "j_match")))
         for k in ("j_generator", "j_topic", "j_gen_index", "j_judge",
                   "j_match", "j_error", "j_time")}
    notes = [f"judgments field map: {f}"]

    d = pd.DataFrame({
        "generator": df[f["j_generator"]],
        "topic": df[f["j_topic"]].astype(str),
        "gen_index": pd.to_numeric(df[f["j_gen_index"]], errors="coerce"),
        "judge": df[f["j_judge"]],
        "match_raw": df[f["j_match"]] if f["j_match"] else np.nan,
    })
    d["_row"] = np.arange(len(d))
    if f["j_time"]:
        d["_time"] = df[f["j_time"]]

    counts = {"raw": len(d)}

    # --- errors -------------------------------------------------------------
    if f["j_error"]:
        errv = df[f["j_error"]]

        def _is_err_val(v):
            if v is None or (isinstance(v, float) and v != v):  # None / NaN
                return False
            return bool(v) and str(v).strip().lower() not in (
                "", "0", "false", "none", "null", "ok", "success", "nan")
        is_err = errv.map(_is_err_val)
    else:
        is_err = pd.Series(False, index=d.index)
    # A missing/NaN verdict is also unusable. Index-aligned assignment BEFORE any sort.
    d["_is_err"] = (is_err | d["match_raw"].isna())
    counts["errors"] = int(d["_is_err"].sum())

    # --- family-disjointness enforced by construction ------------------------
    # A same-family (generator, judge) row can carry a real, non-error verdict —
    # e.g. a pre-substitution judge's response logged rather than discarded —
    # and would pass every other check silently. Every downstream script
    # assumes this precondition rather than re-checking it, so it is enforced
    # here, once, rather than left to audit_counts.py to merely report after
    # the fact. This is exactly the Grok-4.3-substitute contamination pattern
    # noted in project history.
    same_fam = d["generator"].map(family_of) == d["judge"].map(family_of)
    counts["same_family_dropped"] = int((same_fam & ~d["_is_err"]).sum())
    d = d[~same_fam].copy()

    # --- duplicates (keep most recent) --------------------------------------
    # This matches bweird's own load_judgment_records: 2_judge_panel.py's
    # --retry-abstentions appends a fresh record for a key whose earlier
    # attempt failed, and keeping the LAST occurrence per key lets a
    # successful retry supersede its own failure. So a "duplicate" here is
    # usually the earlier, now-superseded error attempt for a key that
    # succeeded on retry — not a second independent verdict — and the two
    # counts (errors, duplicates) are expected to overlap rather than stack.
    key = ["generator", "topic", "gen_index", "judge"]
    sort_col = "_time" if f["j_time"] else "_row"
    d = d.sort_values(sort_col, kind="stable")
    dup_mask_all = d.duplicated(subset=key, keep="last")
    counts["duplicates"] = int(dup_mask_all.sum())
    counts["duplicates_that_were_errors"] = int((dup_mask_all & d["_is_err"]).sum())
    counts["duplicates_that_were_valid"] = int((dup_mask_all & ~d["_is_err"]).sum())

    # order of operations reported both ways for the manuscript:
    counts["valid_before_dedup"] = int((~d["_is_err"]).sum())
    d = d[~dup_mask_all]
    d = d[~d["_is_err"]].copy()
    counts["valid_after_dedup"] = len(d)
    counts["irrecoverable_errors"] = counts["errors"] - counts["duplicates_that_were_errors"]

    # --- canonicalise match values to slots 0..5 ----------------------------
    def to_slot_factory():
        gold_pos = {}
        if gold is not None:
            for _, r in gold.iterrows():
                ids = r["gold_ids"] or []
                gold_pos[str(r["topic"])] = {str(gid): i + 1 for i, gid in enumerate(ids)}

        def to_slot(topic, v):
            if isinstance(v, str):
                vs = v.strip()
            else:
                vs = v
            if vs in CONFIG["no_match_values"] or (isinstance(vs, str)
                    and vs.lower() in {str(x).lower() for x in CONFIG["no_match_values"]}):
                return 0
            # numeric 0..5?
            try:
                iv = int(float(vs))
                if 0 <= iv <= 5:
                    return iv
            except (TypeError, ValueError):
                pass
            # gold id string?
            pos = gold_pos.get(str(topic), {})
            if str(vs) in pos:
                return pos[str(vs)]
            return None  # unresolvable
        return to_slot

    to_slot = to_slot_factory()
    d["match_slot"] = [to_slot(t, v) for t, v in zip(d["topic"], d["match_raw"], strict=False)]
    unresolved = int(d["match_slot"].isna().sum())
    if unresolved:
        ex = d.loc[d["match_slot"].isna(), "match_raw"].astype(str).unique()[:8]
        notes.append(f"WARNING: {unresolved} verdicts had unresolvable match values, "
                     f"e.g. {list(ex)} — treated as dropped. If these are perspective_ids, "
                     f"check gold_v2.json parsing; if positions in a randomised list, the "
                     f"file was not de-randomised and slots cannot be trusted.")
        d = d[~d["match_slot"].isna()]
        counts["unresolved_dropped"] = unresolved
    d["match_slot"] = d["match_slot"].astype(int)

    return d.drop(columns=["match_raw", "_row", "_is_err"], errors="ignore"), counts, notes


def load_generations():
    df = read_jsonl(CONFIG["generations_path"])
    f = {k: resolve_field(df, k) for k in ("g_generator", "g_topic", "g_index")}
    g = pd.DataFrame({
        "generator": df[f["g_generator"]],
        "topic": df[f["g_topic"]].astype(str),
        "index": pd.to_numeric(df[f["g_index"]], errors="coerce"),
    })
    return g, f


def detect_offset(judgments: pd.DataFrame, generations: pd.DataFrame) -> int:
    """Offset to subtract from judgments.gen_index to land on generations.index.
    Known gotcha: judgments are 1-based, generations 0-based -> offset 1."""
    j0, g0 = int(judgments["gen_index"].min()), int(generations["index"].min())
    return j0 - g0


# ----------------------------------------------------------------------------
# Aggregation
# ----------------------------------------------------------------------------
def generation_table(valid: pd.DataFrame) -> pd.DataFrame:
    """Per generated perspective: n_judges, leading verdict, its weight, validity.

    leading  : plurality verdict slot (ties broken toward 0, then lowest slot; conservative)
    weight   : share of that generation's valid judges supporting the leading verdict
    validity : share of that generation's valid judges voting any gold (non-zero) —
               this IS what precision uses, matching bweird's precision_weight exactly,
               since precision doesn't involve the one-to-one assignment at all.

    NOTE: `leading`/`weight` are a per-generation-only summary that ignores the
    per-judge credit-splitting used for actual coverage — they are NOT used
    for coverage (see panel_weights / coverage_per_gold for that) — only for
    precision, and as a lighter-weight proxy in lojo_audit.py and
    human_assignment_audit.py, where "what did this specific generation's
    votes say" is the relevant question rather than the fully split credit.
    """
    recs = []
    tie_count = 0
    for (gen, topic, gi), grp in valid.groupby(["generator", "topic", "gen_index"], sort=False):
        votes = grp["match_slot"].to_numpy()
        n = len(votes)
        vals, cnts = np.unique(votes, return_counts=True)
        mx = cnts.max()
        cands = sorted(vals[cnts == mx].tolist())
        if len(cands) > 1:
            tie_count += 1
            leading = 0 if 0 in cands else cands[0]
        else:
            leading = cands[0]
        recs.append({
            "generator": gen, "topic": topic, "gen_index": gi,
            "n_judges": n,
            "leading": int(leading),
            "weight": float(mx) / n,
            "validity": float((votes != 0).sum()) / n,
        })
    out = pd.DataFrame(recs)
    out.attrs["ties"] = tie_count
    return out


def one_to_one_assign(cell: pd.DataFrame, n_gold: int = 5) -> dict:
    """Reimplementation of bweird.aggregation.greedy_one_to_one + coverage_by_gold.

    CONFIRMED NOT TO BE THE COVERAGE MECHANISM (see panel_weights/coverage_per_gold
    below for that) — verified against real data: this rule's output has a
    consistent, real gap from results/agg/ranking.csv (~2pp, one-directional),
    while the sum-of-panel-weights rule matches ranking.csv to floating-point
    epsilon. This function is real code from aggregation.py, faithfully
    reimplemented, and is kept because greedy_one_to_one's assignments/
    classify_generations almost certainly feed the MATCHED/REDUNDANT/NO_MATCH
    classification behind the deferred gold-standard-expansion clustering
    (Methodology's "Gold incompleteness (descriptive)" paragraph, which
    explicitly says this step "does not alter quantitative model scores") —
    not coverage itself. Not called by coverage_per_gold; kept for that future
    use and so the two mechanisms aren't confused again.

    `cell` is the `valid` rows for ONE (generator, topic): columns judge,
    gen_index, match_slot. Per generation, tally vote share by gold (matches
    only, no-match excluded from the numerator but not the denominator —
    denominator is ALL valid judges for that generation). Build every
    (weight, gold, gen_index) candidate with weight > 0, sort by
    (-weight, gold_id, gen_index), and greedily assign: a candidate is taken
    only if both its gold and its generation are still free, so each
    generation contributes to AT MOST ONE gold and each gold is credited by
    AT MOST ONE generation — a losing generation gets zero, not partial,
    credit, and does not fall back to a weaker gold it also drew votes for
    unless that gold is still unclaimed when its turn comes up in the sort.
    Returns {gold_slot: weight}, 0.0 for any gold nothing was assigned to.
    """
    candidates = []
    for gen_index, grp in cell.groupby("gen_index"):
        denom = len(grp)
        if denom == 0:
            continue
        counts = grp.loc[grp["match_slot"] != 0, "match_slot"].value_counts()
        for gold_slot, c in counts.items():
            w = c / denom
            if w > 0:
                candidates.append((w, int(gold_slot), int(gen_index)))
    candidates.sort(key=lambda t: (-t[0], t[1], t[2]))

    taken_golds, taken_gens, assigned = set(), set(), {}
    for w, gold_slot, gen_index in candidates:
        if gold_slot in taken_golds or gen_index in taken_gens:
            continue
        taken_golds.add(gold_slot)
        taken_gens.add(gen_index)
        assigned[gold_slot] = w
    return {g: assigned.get(g, 0.0) for g in range(1, n_gold + 1)}


def panel_weights(valid: pd.DataFrame) -> pd.DataFrame:
    """The VERIFIED coverage weight, matching the Methodology's existing
    "Aggregation" paragraph exactly (confirmed against results/agg/cells.csv
    and gold_credit.csv to floating-point epsilon) — NOT the one-to-one rule.

    Per judge, independently: if that judge matched k of a topic's
    generations to the same gold, each of those k generations earns 1/k
    credit from that judge toward that gold (0 for every other generation
    that judge rated). A judge's per-gold credit therefore always sums to
    exactly 1 across generations if they matched anything, 0 if they didn't
    — "the unit is shared equally" among however many generations that judge
    thought matched. The panel weight for a (generation, gold) pair is the
    average of this per-judge credit across the judges who rated THAT
    generation (a judge missing on one generation is dropped from that
    cell's average only, per the Aggregation paragraph's "average is taken
    over the judges that remain").

    Returns long table [generator, topic, gen_index, gold_slot, weight],
    densified to all 5 gold slots per generation (0.0 where absent).
    """
    m = valid[valid["match_slot"] != 0].copy()
    # k = how many generations THIS judge matched to THIS gold, within this
    # (generator, topic) cell.
    k = (m.groupby(["generator", "topic", "judge", "match_slot"])["gen_index"]
         .transform("count"))
    m["judge_credit"] = 1.0 / k

    numer = (m.groupby(["generator", "topic", "gen_index", "match_slot"])
             ["judge_credit"].sum().rename("credit_num").reset_index()
             .rename(columns={"match_slot": "gold_slot"}))
    denom = (valid.groupby(["generator", "topic", "gen_index"])["judge"]
             .nunique().rename("n_judges").reset_index())
    out = numer.merge(denom, on=["generator", "topic", "gen_index"])
    out["weight"] = out["credit_num"] / out["n_judges"]

    pairs = valid[["generator", "topic", "gen_index"]].drop_duplicates()
    full = pairs.merge(pd.DataFrame({"gold_slot": [1, 2, 3, 4, 5]}), how="cross")
    dense = full.merge(out[["generator", "topic", "gen_index", "gold_slot", "weight"]],
                       on=["generator", "topic", "gen_index", "gold_slot"], how="left")
    dense["weight"] = dense["weight"].fillna(0.0)
    return dense


def coverage_per_gold(valid: pd.DataFrame) -> pd.DataFrame:
    """Long table [generator, topic, gold_slot, credit]: sum of panel_weights
    across a topic's generations. Structurally bounded in [0,1] already (see
    panel_weights docstring — it's a share of judges, not an unbounded sum),
    so the clip below is a float-safety net, not a load-bearing cap.
    """
    w = panel_weights(valid)
    out = (w.groupby(["generator", "topic", "gold_slot"])["weight"]
           .sum().rename("credit").reset_index())
    out["credit"] = out["credit"].clip(upper=1.0)
    return out


def model_topic_tables(valid: pd.DataFrame, gen_tab: pd.DataFrame):
    """Return (cov_mt, prec_mt, per_gold): per-(model,topic) coverage & precision.

    Coverage: the verified panel_weights/coverage_per_gold rule above.
    Precision is a separate, per-generation quantity — "did any judge match
    this at all" — unaffected by how credit gets split across generations,
    so it still comes from generation_table's validity column (already
    confirmed exact against the real data, 0.0 deviation).
    """
    per_gold = coverage_per_gold(valid)
    cov_mt = (per_gold.groupby(["generator", "topic"])["credit"]
              .mean().rename("coverage").reset_index())
    prec_mt = (gen_tab.groupby(["generator", "topic"])["validity"]
               .mean().rename("precision").reset_index())
    return cov_mt, prec_mt, per_gold


def bootstrap_model_summary(cov_mt, prec_mt, B=10_000, seed=None):
    """Per-model coverage/precision/F1 with percentile bootstrap CIs over topics."""
    seed = CONFIG["seed"] if seed is None else seed
    rng = np.random.default_rng(seed)
    topics = sorted(cov_mt["topic"].unique())
    T = len(topics)
    idx = rng.integers(0, T, size=(B, T))
    rows = []
    for model in sorted(cov_mt["generator"].unique(), key=str):
        c = (cov_mt[cov_mt["generator"] == model].set_index("topic")
             .reindex(topics)["coverage"].to_numpy())
        p = (prec_mt[prec_mt["generator"] == model].set_index("topic")
             .reindex(topics)["precision"].to_numpy())
        cov, prec = float(np.nanmean(c)), float(np.nanmean(p))
        f1 = 2 * cov * prec / (cov + prec) if (cov + prec) else 0.0
        cb, pb = np.nanmean(c[idx], axis=1), np.nanmean(p[idx], axis=1)
        f1b = 2 * cb * pb / (cb + pb)
        lo, hi = (2.5, 97.5)
        rows.append({
            "model": model, "coverage": cov,
            "cov_lo": np.percentile(cb, lo), "cov_hi": np.percentile(cb, hi),
            "precision": prec,
            "prec_lo": np.percentile(pb, lo), "prec_hi": np.percentile(pb, hi),
            "f1": f1, "f1_lo": np.percentile(f1b, lo), "f1_hi": np.percentile(f1b, hi),
        })
    return pd.DataFrame(rows).sort_values("f1", ascending=False).reset_index(drop=True)


# ----------------------------------------------------------------------------
# Stats helpers
# ----------------------------------------------------------------------------
def exact_wilcoxon(deltas, alternative="two-sided"):
    """Exact Wilcoxon signed-rank; returns (stat W+, p, n_effective, rank_biserial)."""
    from scipy import stats
    d = np.asarray(deltas, float)
    d = d[~np.isnan(d)]
    nz = d[d != 0]
    n_eff = len(nz)
    if n_eff == 0:
        return np.nan, 1.0, 0, 0.0
    try:
        res = stats.wilcoxon(d, alternative=alternative, method="exact")
    except (TypeError, ValueError):
        try:
            res = stats.wilcoxon(d, alternative=alternative, mode="exact")
        except (TypeError, ValueError):
            res = stats.wilcoxon(d, alternative=alternative)
    # Compute W+ ourselves: scipy's `statistic` convention depends on `alternative`
    # (two-sided returns min(W+, W-)), which flips the effect-size sign.
    ranks = stats.rankdata(np.abs(nz))
    wplus = float(ranks[nz > 0].sum())
    total = n_eff * (n_eff + 1) / 2
    r_rb = (2 * wplus - total) / total
    return wplus, float(res.pvalue), n_eff, float(r_rb)


def bh_adjust(pvals):
    p = np.asarray(pvals, float)
    m = len(p)
    order = np.argsort(p)
    adj = p[order] * m / (np.arange(m) + 1)
    adj = np.minimum.accumulate(adj[::-1])[::-1]
    out = np.empty(m)
    out[order] = np.clip(adj, 0, 1)
    return out


def pair_deltas(cov_mt: pd.DataFrame, gold: pd.DataFrame) -> pd.DataFrame:
    """Per (model, pair): coverage_WEIRD - coverage_SERBIAN."""
    meta = gold[["topic", "pair", "arm"]].dropna(subset=["pair", "arm"])
    meta["topic"] = meta["topic"].astype(str)
    d = cov_mt.merge(meta, on="topic", how="left")
    missing = d[d["pair"].isna()]["topic"].unique()
    if len(missing):
        raise SystemExit(
            f"No pair/arm metadata for topics {list(missing)}.\n"
            f"Fill CONFIG['manual_topic_map'] in bw_common.py (run --inspect for a stub).")
    piv = d.pivot_table(index=["generator", "pair"], columns="arm",
                        values="coverage", aggfunc="mean").reset_index()
    for col in ("WEIRD", "SERBIAN"):
        if col not in piv.columns:
            raise SystemExit(f"Arm label {col!r} absent after normalisation; "
                             f"check CONFIG['arm_normalize'] / gold file arms.")
    piv["delta"] = piv["WEIRD"] - piv["SERBIAN"]
    return piv


# ----------------------------------------------------------------------------
# One-stop loader used by the driver scripts
# ----------------------------------------------------------------------------
def load_all(verbose=True):
    gold = load_gold()
    valid, counts, notes = load_judgments(gold)
    gen_tab = generation_table(valid)
    cov_mt, prec_mt, per_gold = model_topic_tables(valid, gen_tab)
    if verbose:
        fam_note = (f" same_family_dropped={counts['same_family_dropped']}"
                    if counts.get("same_family_dropped") else "")
        print(f"[bw_common] verdicts: raw={counts['raw']} errors={counts['errors']}"
              f"{fam_note} dups={counts['duplicates']} "
              f"valid_after_dedup={counts['valid_after_dedup']}  "
              f"generations={len(gen_tab)}  plurality ties={gen_tab.attrs.get('ties', 0)}")
        for n in notes:
            print("[bw_common]", n)
    return {"gold": gold, "valid": valid, "gen_tab": gen_tab, "cov_mt": cov_mt,
            "prec_mt": prec_mt, "per_gold": per_gold, "counts": counts}


# ----------------------------------------------------------------------------
# --inspect
# ----------------------------------------------------------------------------
def _inspect():
    print("=" * 78)
    print("INSPECT: schema detection and sanity checks")
    print("=" * 78)

    jdf = read_jsonl(CONFIG["judgments_path"])
    print(f"\njudgments.jsonl  rows={len(jdf)}  (published raw count: "
          f"{PUBLISHED_COUNTS['raw']})")
    print("columns:", list(jdf.columns))
    print("sample:", json.dumps(jdf.iloc[0].to_dict(), default=str)[:400])
    fmap = {}
    for k in ("j_generator", "j_topic", "j_gen_index", "j_judge", "j_match",
              "j_error", "j_time"):
        try:
            fmap[k] = resolve_field(jdf, k, required=False)
        except SystemExit as e:
            fmap[k] = f"!! {e}"
    print("detected fields:", fmap)

    gdf = read_jsonl(CONFIG["generations_path"])
    print(f"\ngenerations.jsonl  rows={len(gdf)}  (expected 1,040 = 13x16x5)")
    print("columns:", list(gdf.columns))
    gmap = {k: resolve_field(gdf, k, required=False)
            for k in ("g_generator", "g_topic", "g_index")}
    print("detected fields:", gmap)

    if fmap.get("j_gen_index") and gmap.get("g_index"):
        jmin = pd.to_numeric(jdf[fmap["j_gen_index"]], errors="coerce").min()
        gmin = pd.to_numeric(gdf[gmap["g_index"]], errors="coerce").min()
        print(f"\nindex bases: judgments min={jmin}  generations min={gmin}  "
              f"-> join offset = {int(jmin - gmin)} "
              f"(expected 1: judgments 1-based, generations 0-based)")

    if fmap.get("j_generator"):
        gens = sorted(jdf[fmap["j_generator"]].astype(str).unique())
        print(f"\ngenerators in judgments ({len(gens)}, expected 13):")
        for g in gens:
            print(f"  {g:45s} -> published: {published_label(g)}  family: {family_of(g)}")
    if fmap.get("j_judge"):
        js = sorted(jdf[fmap["j_judge"]].astype(str).unique())
        print(f"\njudges in judgments ({len(js)}, expected 7 = 5 base + 2 substitutes):")
        for j in js:
            print(f"  {j:45s} family: {family_of(j)}")
    if fmap.get("j_match"):
        vals = jdf[fmap["j_match"]].astype(str).value_counts()
        print(f"\nmatch value distribution (top 12):\n{vals.head(12).to_string()}")
        n_null = jdf[fmap["j_match"]].isna().sum()
        print(f"null/NaN in match field: {n_null} (currently treated as ERRORS, not "
              f"no-match — verify this is right for your schema; see the diagnostic "
              f"snippet in chat if match_gold_id can be null for reasons other than "
              f"a failed judge call)")

    extra = [c for c in jdf.columns if c not in fmap.values() and c is not None]
    if "role" in extra:
        print(f"\n'role' column present (not used by any script yet): "
              f"{jdf['role'].value_counts().to_dict()}")
        print("If this has more than one value, some rows may be logged-but-excluded "
              "panel members (e.g. a same-family judge dropped in favour of a "
              "substitute) rather than duplicates — flag this before trusting counts.")
    jpg = jdf.groupby([fmap.get("j_generator"), fmap.get("j_topic"),
                       fmap.get("j_gen_index")]).size() if fmap.get("j_generator") else None
    if jpg is not None:
        dist = jpg.value_counts().sort_index()
        print(f"\nraw rows per (generator, topic, gen_index) BEFORE any cleaning "
              f"(expect a spike at 5, anything at 6+ suggests panel-composition "
              f"contamination):\n{dist.to_string()}")

    try:
        gold = load_gold()
        print(f"\ngold topics parsed: {len(gold)} (expected 16); "
              f"golds/topic: {sorted({len(x) for x in gold['gold_ids']})}")
        need_map = gold["pair"].isna().any() or gold["arm"].isna().any()
        print(gold[["topic", "pair", "arm"]].to_string(index=False))
        if need_map:
            print("\npair/arm missing for some topics. Paste into "
                  "CONFIG['manual_topic_map'] and fill in:")
            stub = {str(t): {"pair": "pairXX", "arm": "WEIRD|SERBIAN"}
                    for t in gold.loc[gold["pair"].isna() | gold["arm"].isna(), "topic"]}
            print(json.dumps(stub, indent=2))
    except SystemExit as e:
        print(f"\ngold parsing failed: {e}")

    print("\nIf every guess above is right, proceed to audit_counts.py. "
          "Otherwise set CONFIG['fields'] / manual_topic_map and re-run.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--inspect", action="store_true",
                    help="print schema detection and sanity checks")
    args = ap.parse_args()
    if args.inspect:
        _inspect()
    else:
        ap.print_help()
