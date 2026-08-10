"""topic_difficulty.py — per-topic coverage + per-pair Table 5 (step 11).

Computes per-topic coverage averaged over the thirteen generators, the full
16-topic difficulty ranking, and the eight-row matched-pair table (WEIRD topic,
Serbian topic, delta in pp). Prints paste-ready markdown and writes CSVs.

Run:  python topic_difficulty.py
"""
import pandas as pd

import bw_common as bw


def main():
    data = bw.load_all()
    gold = data["gold"]
    cov_mt = data["cov_mt"]
    outdir = bw._outdir()

    meta = gold[["topic", "pair", "arm"]].copy()
    meta["topic"] = meta["topic"].astype(str)
    d = cov_mt.merge(meta, on="topic", how="left")

    # ---- full 16-topic ranking --------------------------------------------
    per_topic = (d.groupby(["topic", "pair", "arm"], dropna=False)["coverage"]
                 .agg(["mean", "std", "count"]).reset_index()
                 .rename(columns={"mean": "coverage", "std": "sd_models",
                                  "count": "n_models"})
                 .sort_values("coverage"))
    print("\n" + "=" * 78)
    print("PER-TOPIC COVERAGE (mean over models), hardest first")
    print("=" * 78)
    for _, r in per_topic.iterrows():
        print(f"  {str(r['topic']):<42s} {str(r['arm'] or '?'):<8s} "
              f"pair={str(r['pair'] or '?'):<8s} {r['coverage']:.3f} "
              f"(sd {r['sd_models']:.3f}, n={int(r['n_models'])})")

    hard, easy = per_topic.iloc[0], per_topic.iloc[-1]
    spread = easy["coverage"] - hard["coverage"]
    print(f"\nhardest: {hard['topic']} ({hard['coverage']:.3f})   "
          f"easiest: {easy['topic']} ({easy['coverage']:.3f})   "
          f"topic spread: {spread:.3f} ({spread*100:.1f} pp)")
    print("published check: hardest 0.449, easiest 0.685, both Serbian; "
          "WEIRD span 0.465-0.640")
    for arm in ("WEIRD", "SERBIAN"):
        sub = per_topic[per_topic["arm"] == arm]
        if len(sub):
            print(f"  {arm} span: {sub['coverage'].min():.3f}-"
                  f"{sub['coverage'].max():.3f}")

    # ---- Table 5: matched pairs -------------------------------------------
    ok = per_topic.dropna(subset=["pair", "arm"])
    piv = ok.pivot_table(index="pair", columns="arm", values="coverage",
                         aggfunc="mean")
    names = ok.pivot_table(index="pair", columns="arm", values="topic",
                           aggfunc="first")
    t5 = pd.DataFrame({
        "pair": piv.index,
        "weird_topic": names.get("WEIRD"),
        "weird_cov": piv.get("WEIRD"),
        "serbian_topic": names.get("SERBIAN"),
        "serbian_cov": piv.get("SERBIAN"),
    }).reset_index(drop=True)
    t5["delta_pp"] = (t5["weird_cov"] - t5["serbian_cov"]) * 100
    t5 = t5.sort_values("pair").reset_index(drop=True)

    print("\n" + "=" * 78)
    print("TABLE 5 — matched pairs (delta = WEIRD - Serbian, percentage points)")
    print("=" * 78)
    hdr = "| Pair | WEIRD topic | Cov. | Serbian topic | Cov. | Δ (pp) |"
    sep = "|---|---|---|---|---|---|"
    print(hdr); print(sep)
    for _, r in t5.iterrows():
        print(f"| {r['pair']} | {r['weird_topic']} | {r['weird_cov']:.3f} "
              f"| {r['serbian_topic']} | {r['serbian_cov']:.3f} "
              f"| {r['delta_pp']:+.1f} |")
    print(f"| **Mean** |  | {t5['weird_cov'].mean():.3f} |  "
          f"| {t5['serbian_cov'].mean():.3f} | {t5['delta_pp'].mean():+.1f} |")

    small = int((t5["delta_pp"].abs() <= 6).sum())
    print(f"\nnarrative checks: pairs with |Δ| <= 6 pp: {small}/8 (published: 5/8); "
          f"largest two deltas: "
          f"{t5.loc[t5['delta_pp'].abs().nlargest(2).index, 'delta_pp'].round(1).tolist()} "
          f"(published: +19 and -17, opposite signs); mean Δ "
          f"{t5['delta_pp'].mean():+.1f} pp (published: -1.3)")

    p1 = outdir / "per_topic_coverage.csv"
    per_topic.to_csv(p1, index=False)
    p2 = outdir / "table5_matched_pairs.csv"
    t5.to_csv(p2, index=False)
    print(f"\nwrote {p1}\nwrote {p2}")
    print("\nPaste the two blocks above back into the chat and I will draft the "
          "topic-difficulty subsection around them.")


if __name__ == "__main__":
    main()
