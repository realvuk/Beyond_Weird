"""human_assignment_audit.py — salvaged human check, split by arm (step 12).

The dropped validation sheet lacked a no-match option, so it cannot validate
match/no-match decisions — but on items the PANEL confidently matched, the
human's forced five-way choice still validates WHICH gold gets assigned
(chance = 20%). This script computes that agreement overall and per arm; the
per-arm split is what patches the equal-reliability-vs-equal-validity gap in
Section 4.5.

Edit CONFIG_H below, then run:  python human_assignment_audit.py
"""
from pathlib import Path

import pandas as pd
from scipy import stats

import bw_common as bw

# ---------------------------------------------------------------------------
CONFIG_H = {
    # Built by build_human_assignment_input.py from annotations_adjudicated.csv;
    # see that script for what the construction assumes.
    "human_path": str(bw.ROOT / "results" / "annotation" / "human_annotations.csv"),
    # column names in the human file (None = try the same candidates as judgments)
    "fields": {
        "generator": None,      # generator model of the annotated perspective
        "topic": None,
        "gen_index": None,      # index of the generated perspective
        "label": None,          # the human's chosen gold (1..5 or perspective_id)
        "annotator": None,      # optional; if present, rows are per annotator
    },
    "gen_index_base": 1,        # 1 if the sheet used judgments' 1-based indexing, else 0
    "min_weight": 0.8,          # panel agreement threshold defining 'high-confidence'
}
# ---------------------------------------------------------------------------

_CAND = {
    "generator": ["generator", "model", "gen_model", "generator_model"],
    "topic": ["topic", "topic_id", "topic_title"],
    "gen_index": ["gen_index", "generation_index", "perspective_index", "index"],
    "label": ["label", "human", "human_label", "gold", "gold_index", "choice",
              "annotation", "match"],
    "annotator": ["annotator", "rater", "coder", "annotator_id"],
}


def load_human():
    p = Path(CONFIG_H["human_path"])
    if not p.exists():
        raise SystemExit(f"{p} not found — set CONFIG_H['human_path'].")
    df = (bw.read_jsonl(p) if p.suffix.lower() == ".jsonl"
          else pd.read_csv(p))
    cols = {}
    for k, cands in _CAND.items():
        v = CONFIG_H["fields"].get(k)
        if v is None:
            v = next((c for c in cands if c in df.columns), None)
        if v is None and k != "annotator":
            raise SystemExit(f"Could not find a '{k}' column in {list(df.columns)}; "
                             f"set CONFIG_H['fields'].")
        cols[k] = v
    out = pd.DataFrame({
        "generator": df[cols["generator"]],
        "topic": df[cols["topic"]].astype(str),
        "gen_index": pd.to_numeric(df[cols["gen_index"]], errors="coerce"),
        "human_raw": df[cols["label"]],
    })
    if cols.get("annotator"):
        out["annotator"] = df[cols["annotator"]]
    # align to judgments' index base
    shift = 1 - CONFIG_H["gen_index_base"]
    out["gen_index"] = out["gen_index"] + shift
    return out


def main():
    data = bw.load_all()
    gold, gen_tab = data["gold"], data["gen_tab"]

    human = load_human()

    # canonicalise human labels to slots using the same machinery
    gold_pos = {str(r["topic"]): {str(g): i + 1 for i, g in enumerate(r["gold_ids"] or [])}
                for _, r in gold.iterrows()}

    def to_slot(topic, v):
        try:
            iv = int(float(v))
            if 1 <= iv <= 5:
                return iv
            if iv == 0:
                return 0
        except (TypeError, ValueError):
            pass
        return gold_pos.get(str(topic), {}).get(str(v).strip())

    human["human_slot"] = [to_slot(t, v) for t, v in
                           zip(human["topic"], human["human_raw"], strict=False)]
    bad = human["human_slot"].isna().sum()
    if bad:
        print(f"WARNING: {bad} human labels unresolvable; dropped.")
        human = human.dropna(subset=["human_slot"])

    panel = gen_tab[["generator", "topic", "gen_index", "leading", "weight"]]
    m = human.merge(panel, on=["generator", "topic", "gen_index"], how="left")
    unmatched = m["leading"].isna().sum()
    if unmatched:
        print(f"WARNING: {unmatched} annotated rows found no panel verdict — check "
              f"CONFIG_H['gen_index_base'] and the generator/topic strings.")
        m = m.dropna(subset=["leading"])

    hi = m[(m["leading"] != 0) & (m["weight"] >= CONFIG_H["min_weight"])].copy()
    hi["agree"] = hi["human_slot"] == hi["leading"]

    meta = gold[["topic", "arm"]].copy()
    meta["topic"] = meta["topic"].astype(str)
    hi = hi.merge(meta, on="topic", how="left")

    def report(sub, name):
        n = len(sub)
        if n == 0:
            print(f"{name:10s} n=0")
            return
        k = int(sub["agree"].sum())
        bt = stats.binomtest(k, n, p=0.2, alternative="greater")
        ci = bt.proportion_ci(confidence_level=0.95, method="exact")
        print(f"{name:10s} n={n:4d}  agreement={k/n:.1%}  "
              f"95% CI [{ci.low:.1%}, {ci.high:.1%}]  "
              f"p(vs 20% chance)={bt.pvalue:.2e}")

    print("\n" + "=" * 78)
    print(f"ASSIGNMENT AUDIT — panel matches with agreement weight >= "
          f"{CONFIG_H['min_weight']} (forced 5-way choice, chance 20%)")
    print("=" * 78)
    if "annotator" in hi.columns:
        for a, sub in hi.groupby("annotator"):
            print(f"\nannotator: {a}")
            report(sub, "overall")
            for arm in ("WEIRD", "SERBIAN"):
                report(sub[sub["arm"] == arm], arm)
    else:
        report(hi, "overall")
        for arm in ("WEIRD", "SERBIAN"):
            report(hi[hi["arm"] == arm], arm)

    out = bw._outdir() / "human_assignment_audit.csv"
    hi.to_csv(out, index=False)
    print(f"\nwrote {out}")
    print("\nIf WEIRD and Serbian agreement are comparable, that sentence goes into "
          "4.5 as the arm-specific validity check replacing the dangling "
          "'arm-specific comparison against human annotation' promise.")


if __name__ == "__main__":
    main()
