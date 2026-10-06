#!/usr/bin/env python3
"""
eval_reliability.py — Step 7: judge reliability and bias control.

Four analyses, per the Methodology:

1. INTER-JUDGE AGREEMENT. Fleiss' kappa, plus Gwet's AC1 and Krippendorff's
   alpha (robust under the skewed no-match marginal / kappa paradox).
   Items = (generator, topic, generation) scored by the family-disjoint
   panel; labels are mapped to a shared 6-category space (gold position 1-5
   within the topic's canonical order, plus "0" for no-match) so agreement
   is computable across topics. Items need >=2 ok verdicts (alpha handles
   variable raters natively; kappa/AC1 use the variable-rater
   generalisations). Reported pooled and separately for each arm.
   Pairwise Cohen's kappa between judges is reported alongside it; it
   depends only on panel verdicts, so it does not require --human.

2. VALIDITY AGAINST HUMANS. Requires --human annotations CSV with columns:
   generator, topic_id, generation_id, annotator_1, annotator_2, adjudicated
   (labels = canonical gold_id or "0"). Reports raw inter-annotator agreement
   and Cohen's kappa (human ceiling); panel plurality-verdict accuracy against
   the adjudicated labels; error decomposition into misses (panel 0, human
   gold), misassignments (panel gold_a, human gold_b) and false alarms (panel
   gold, human 0); and a Wilcoxon rank-sum (Mann-Whitney) test comparing
   panel agreement weights on items where the annotators agreed vs disagreed.

3. PER-JUDGE AUDIT. Each judge individually vs the adjudicated labels; the
   panel must outperform its best single member; leave-one-judge-out panel
   accuracy.

4. BIAS CONTROL. Coverage under the full base panel vs the family-disjoint
   panel, for every generator whose family sits on the base panel. Requires
   verdicts from BOTH the own-family judge and its substitute on the same
   generations. Reports per-generator and per-family deltas
   (full - disjoint, in coverage points) with topic-bootstrap CIs.

Usage:
  python eval_reliability.py --verdicts verdicts.jsonl --topics topics.json \
      --panels panels.json --out out/ [--human human_annotations.csv]
"""
import argparse
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu

from bweird.analysis import (
    ADAPTED_DIR,
    AGG_DIR,
    NO_MATCH,
    aggregate_all,
    cohen_kappa,
    fleiss_kappa,
    gwet_ac1,
    krippendorff_alpha,
    load_eval_topics,
    load_panels,
    load_verdicts,
    log,
    observed_agreement,
    plurality_verdict,
    resolve_panel,
)
from bweird.logging_utils import run_stage


def positional(label, topics, topic_id):
    """Map canonical gold_id (or '0'/None/NaN) to shared positional label '0'-'5'."""
    if label is None or pd.isna(label) or str(label) == NO_MATCH:
        return NO_MATCH
    return str(topics[topic_id]["gold_ids"].index(label) + 1)


def panel_verdicts(verdicts, topics, panels, config="disjoint"):
    """Ok verdicts restricted to each generator's scoring panel, with
    positional labels. Returns tidy DataFrame."""
    frames = []
    for g, sub in verdicts.groupby("generator"):
        panel = resolve_panel(g, panels, config)
        sub = sub[(sub.judge.isin(panel)) & (sub.status == "ok")].copy()
        sub["pos_label"] = [positional(m, topics, t)
                            for m, t in zip(sub.match, sub.topic_id, strict=False)]
        frames.append(sub)
    return pd.concat(frames, ignore_index=True)


# ------------------------------------------------------------------ analyses

def inter_judge_agreement(pv):
    items = [Counter(g.pos_label)
             for _, g in pv.groupby(["generator", "topic_id", "generation_id"])]
    return {
        "n_items": len([i for i in items if sum(i.values()) >= 2]),
        "n_verdicts": len(pv),
        "no_match_rate": float((pv.pos_label == NO_MATCH).mean()),
        "observed_agreement": observed_agreement(items),
        "fleiss_kappa": fleiss_kappa(items),
        "gwet_ac1": gwet_ac1(items),
        "krippendorff_alpha": krippendorff_alpha(items),
    }


def pairwise_judge_kappa(pv):
    """Pairwise Cohen's kappa between judges on the items they jointly scored.
    Depends only on panel verdicts — no human annotations required."""
    key = ["generator", "topic_id", "generation_id"]
    piv = pv.pivot_table(index=key, columns="judge", values="pos_label",
                         aggfunc="first")
    judges = sorted(pv.judge.unique())
    pk = pd.DataFrame(index=judges, columns=judges, dtype=float)
    n = pd.DataFrame(index=judges, columns=judges, dtype=float)
    for i, a in enumerate(judges):
        for b in judges[i:]:
            both = piv[[a, b]].dropna()
            k = 1.0 if a == b else cohen_kappa(both[a].tolist(), both[b].tolist())
            pk.loc[a, b] = pk.loc[b, a] = k
            n.loc[a, b] = n.loc[b, a] = len(both)
    return pk, n


def human_validation(pv, human, topics, out):
    key = ["generator", "topic_id", "generation_id"]
    human = human.copy()
    for col in ("annotator_1", "annotator_2", "adjudicated"):
        human[col] = [positional(v if str(v) != "0" else None, topics, t)
                      for v, t in zip(human[col].astype(str), human.topic_id, strict=False)]
    # panel plurality + weight per annotated item
    rows = []
    grouped = pv.groupby(key)
    for _, h in human.iterrows():
        k = (h.generator, h.topic_id, str(h.generation_id))
        if k not in grouped.groups:
            log.warning("annotated item %s has no panel verdicts; skipped", k)
            continue
        labels = grouped.get_group(k).pos_label.tolist()
        verdict, weight = plurality_verdict(labels)
        rows.append({**{c: v for c, v in zip(key, k, strict=False)},
                     "panel_verdict": verdict, "panel_weight": weight,
                     "annotator_1": h.annotator_1, "annotator_2": h.annotator_2,
                     "adjudicated": h.adjudicated})
    dv = pd.DataFrame(rows)
    if dv.empty:
        log.warning("no annotated items matched panel verdicts")
        return None

    iaa_pct = float((dv.annotator_1 == dv.annotator_2).mean())
    iaa_kappa = cohen_kappa(dv.annotator_1.tolist(), dv.annotator_2.tolist())
    acc = float((dv.panel_verdict == dv.adjudicated).mean())

    err = dv[dv.panel_verdict != dv.adjudicated]
    miss = int(((err.panel_verdict == NO_MATCH) & (err.adjudicated != NO_MATCH)).sum())
    false_alarm = int(((err.panel_verdict != NO_MATCH) & (err.adjudicated == NO_MATCH)).sum())
    misassign = len(err) - miss - false_alarm

    agree_w = dv.loc[dv.annotator_1 == dv.annotator_2, "panel_weight"]
    disagree_w = dv.loc[dv.annotator_1 != dv.annotator_2, "panel_weight"]
    if len(agree_w) and len(disagree_w):
        u, p = mannwhitneyu(agree_w, disagree_w, alternative="two-sided")
        wilcox = {"U": float(u), "p": float(p),
                  "median_weight_agree": float(agree_w.median()),
                  "median_weight_disagree": float(disagree_w.median()),
                  "n_agree": len(agree_w), "n_disagree": len(disagree_w)}
    else:
        wilcox = {"note": "one of the strata is empty; test skipped"}

    dv.to_csv(out / "human_validation_items.csv", index=False)
    return {"n_annotated": len(dv),
            "inter_annotator_pct": iaa_pct, "inter_annotator_kappa": iaa_kappa,
            "panel_accuracy_vs_adjudicated": acc,
            "errors": {"total": len(err), "misses": miss,
                       "misassignments": misassign, "false_alarms": false_alarm},
            "weight_vs_human_disagreement": wilcox}


def per_judge_audit(pv, human_items):
    """human_items: DataFrame from human_validation_items.csv (positional labels)."""
    key = ["generator", "topic_id", "generation_id"]
    merged = pv.merge(human_items[key + ["adjudicated"]], on=key, how="inner")

    per_judge = (merged.assign(correct=lambda d: d.pos_label == d.adjudicated)
                 .groupby("judge").agg(accuracy=("correct", "mean"),
                                       n=("correct", "size")).reset_index()
                 .sort_values("accuracy", ascending=False))

    # panel and leave-one-judge-out plurality accuracy on the annotated items
    def plur_acc(exclude=None):
        hits, tot = 0, 0
        for _key, g in merged.groupby(key):
            labels = g.loc[g.judge != exclude, "pos_label"].tolist()
            if not labels:
                continue
            v, _ = plurality_verdict(labels)
            hits += (v == g.adjudicated.iloc[0])
            tot += 1
        return hits / tot if tot else float("nan")

    panel_acc = plur_acc()
    lojo = pd.DataFrame([{"left_out": j, "panel_accuracy_without": plur_acc(j)}
                         for j in sorted(merged.judge.unique())])
    lojo["delta_vs_full"] = lojo.panel_accuracy_without - panel_acc

    return per_judge, panel_acc, lojo


def bias_control(verdicts, topics, panels, out, n_boot=10000, seed=42):
    fam = panels["families"]
    panel_fams = {fam[j] for j in panels["base_panel"]}
    gens = [g for g in sorted(verdicts.generator.unique())
            if fam.get(g) in panel_fams]
    if not gens:
        return None
    # The "full" panel is only a same-family comparison if own-family verdicts
    # were actually collected (2_judge_panel.py --include-family-probe). Without
    # them this silently degrades to 4 base judges vs 5, which looks like a
    # publishable null but says nothing about same-family bias.
    own_family = verdicts[[fam.get(j) == fam.get(g)
                           for j, g in zip(verdicts.judge, verdicts.generator, strict=False)]]
    if own_family.empty:
        log.warning("no same-family verdicts in the input: bias control would "
                    "compare 4 judges against 5, not own-family against "
                    "substitute. Skipped. Rerun 2_judge_panel.py with "
                    "--include-family-probe to measure this for real.")
        return None
    cov_d = aggregate_all(verdicts, topics, panels, "disjoint", gens)["coverage_topic"]
    cov_f = aggregate_all(verdicts, topics, panels, "full", gens)["coverage_topic"]
    m = cov_f.merge(cov_d, on=["generator", "topic_id"], suffixes=("_full", "_disjoint"))
    m["delta"] = m.coverage_sum_full - m.coverage_sum_disjoint
    m["family"] = m.generator.map(fam)

    rng = np.random.default_rng(seed)
    rows = []
    for level, keycol in (("generator", "generator"), ("family", "family")):
        for k, sub in m.groupby(keycol):
            d = sub.delta.to_numpy(float)
            idx = rng.integers(0, len(d), size=(n_boot, len(d)))
            boots = d[idx].mean(axis=1)
            lo, hi = np.percentile(boots, [2.5, 97.5])
            rows.append((level, k, float(d.mean()), float(lo), float(hi), len(d)))
    res = pd.DataFrame(rows, columns=["level", "unit", "delta_full_minus_disjoint",
                                      "ci_lo", "ci_hi", "n_units"])
    m.to_csv(out / "bias_per_topic.csv", index=False)
    res.to_csv(out / "bias_summary.csv", index=False)
    return res


# --------------------------------------------------------------------- main

def build_arg_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verdicts", default=str(ADAPTED_DIR / "verdicts.jsonl"))
    ap.add_argument("--topics", default=str(ADAPTED_DIR / "topics.json"))
    ap.add_argument("--panels", default=str(ADAPTED_DIR / "panels.json"))
    ap.add_argument("--out", default=str(AGG_DIR))
    ap.add_argument("--human", help="human annotations CSV (see docstring)")
    ap.add_argument("--n-boot", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=42)
    return ap


def run(args: argparse.Namespace) -> int:
    topics = load_eval_topics(args.topics)
    panels = load_panels(args.panels)
    verdicts = load_verdicts(args.verdicts, topics)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    pv = panel_verdicts(verdicts, topics, panels, "disjoint")

    print("\n=== 1. Inter-judge agreement (family-disjoint panels) ===")
    arm = pv.topic_id.map(lambda t: topics[t]["arm"])
    agr = pd.DataFrame([
        {"scope": scope, **inter_judge_agreement(sub)}
        for scope, sub in (("all", pv), ("weird", pv[arm == "weird"]),
                           ("serbian", pv[arm == "serbian"]))
    ])
    print(agr.round(4).to_string(index=False))
    agr.to_csv(out / "inter_judge_agreement.csv", index=False)

    print("\n=== 1b. Pairwise judge agreement (Cohen's kappa) ===")
    pk, pk_n = pairwise_judge_kappa(pv)
    print(pk.round(3).to_string())
    pk.to_csv(out / "pairwise_judge_kappa.csv")
    pk_n.astype(int).to_csv(out / "pairwise_judge_overlap.csv")

    print("\n=== 1c. Per-judge match rate (share of valid decisions matched to a reference) ===")
    jm = pv.groupby("judge").match.agg(n_decisions="size", match_rate=lambda s: s.notna().mean())
    print(jm.round(3).to_string())
    jm.to_csv(out / "judge_match_rates.csv")

    hv = None
    if args.human:
        print("\n=== 2. Validity against humans ===")
        human = pd.read_csv(args.human, dtype=str)
        hv = human_validation(pv, human, topics, out)
        if hv:
            print(f"  annotated items                {hv['n_annotated']}")
            print(f"  inter-annotator agreement      {hv['inter_annotator_pct']:.3f} "
                  f"(Cohen's kappa {hv['inter_annotator_kappa']:.3f})  <- human ceiling")
            print(f"  panel plurality accuracy       {hv['panel_accuracy_vs_adjudicated']:.3f}")
            e = hv["errors"]
            print(f"  errors: {e['total']} = {e['misses']} misses + "
                  f"{e['misassignments']} misassignments + {e['false_alarms']} false alarms")
            w = hv["weight_vs_human_disagreement"]
            if "p" in w:
                print(f"  panel weight, human-agree vs human-disagree items: "
                      f"medians {w['median_weight_agree']:.2f} vs "
                      f"{w['median_weight_disagree']:.2f}, "
                      f"Mann-Whitney U={w['U']:.1f}, p={w['p']:.4f}")

            print("\n=== 3. Per-judge audit (vs adjudicated labels) ===")
            items = pd.read_csv(out / "human_validation_items.csv", dtype=str)
            per_judge, panel_acc, lojo = per_judge_audit(pv, items)
            print(per_judge.round(3).to_string(index=False))
            best = per_judge.accuracy.max()
            print(f"  panel plurality accuracy {panel_acc:.3f} vs best single judge "
                  f"{best:.3f} -> panel "
                  f"{'OUTPERFORMS' if panel_acc > best else 'does NOT outperform'}")
            print("  leave-one-judge-out:")
            print(lojo.round(3).to_string(index=False))
            per_judge.to_csv(out / "per_judge_accuracy.csv", index=False)
            lojo.to_csv(out / "leave_one_judge_out.csv", index=False)
    else:
        print("\n(no --human file: analyses 2 and 3 skipped)")

    print("\n=== 4. Bias control: full panel vs family-disjoint panel ===")
    bias = bias_control(verdicts, topics, panels, out,
                        n_boot=args.n_boot, seed=args.seed)
    if bias is None:
        print("  skipped -- see warning above (no same-family generators, or no "
              "same-family verdicts to compare against)")
    else:
        disp = bias.copy()
        for c in ("delta_full_minus_disjoint", "ci_lo", "ci_hi"):
            disp[c] = disp[c].round(4)
        print(disp.to_string(index=False))
        print("  (positive delta = own-family judge inflates coverage)")

    print(f"\nArtifacts written to {out}/")
    return 0


def main(argv: list[str] | None = None) -> int:
    return run_stage(build_arg_parser(), run, argv)


if __name__ == "__main__":
    sys.exit(main())
