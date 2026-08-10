"""audit_counts.py — verdict accounting for Results 4.1/4.5 (step 2).

Resolves exactly which N the analyses run on: raw verdicts, API errors,
duplicates, and the count after both are removed. Also checks the evaluation
grid (13 x 16 x 5 generations, 5 judges each) and family-disjointness.

Run:  python audit_counts.py
"""

import bw_common as bw


def main():
    gold = bw.load_gold()
    valid, counts, notes = bw.load_judgments(gold)
    for n in notes:
        print("[note]", n)

    print("=" * 78)
    print("VERDICT ACCOUNTING")
    print("=" * 78)
    exp = 13 * 16 * 5 * 5
    print(f"expected grid           : 13 models x 16 topics x 5 gens x 5 judges = {exp}")
    print(f"raw verdicts in file    : {counts['raw']:>5}   (published: "
          f"{bw.PUBLISHED_COUNTS['raw']})")
    print(f"API errors / no verdict : {counts['errors']:>5}   (published: "
          f"{bw.PUBLISHED_COUNTS['errors']})")
    if counts.get("same_family_dropped"):
        print(f"same-family, non-error rows dropped: {counts['same_family_dropped']:>5}   "
              f"(a logged pre-substitution judge verdict, not an API error — removed "
              f"before dedup so it can never masquerade as a valid 6th judge)")
    print(f"duplicate verdicts      : {counts['duplicates']:>5}   (published: "
          f"{bw.PUBLISHED_COUNTS['duplicates']}; kept most recent)")
    if counts["duplicates"]:
        print(f"  of which retry-superseded errors: {counts['duplicates_that_were_errors']:>5}"
              f"   (earlier failed attempt, later attempt at the same key succeeded — "
              f"expected and harmless)")
        print(f"  of which genuine valid duplicates: {counts['duplicates_that_were_valid']:>5}"
              f"   (two full successful verdicts for the same key — investigate if > 0,"
              f" this is NOT explained by retry-on-failure)")
    print(f"irrecoverable errors    : {counts['irrecoverable_errors']:>5}   "
          f"(the {counts['errors']} raw errors minus the "
          f"{counts['duplicates_that_were_errors']} that got a successful retry — this "
          f"is the number of generations that end up with only 4 of 5 judges)")
    print(f"valid, before removing duplicate-flagged rows : {counts['valid_before_dedup']:>5}")
    print(f"valid, final (after dedup)                    : {counts['valid_after_dedup']:>5}"
          f"   <- the N every analysis in this pack uses")
    if counts.get("unresolved_dropped"):
        print(f"unresolvable matches    : {counts['unresolved_dropped']:>5}   (dropped; "
              f"see warning above)")
    print("\nManuscript sentence check: valid_before_dedup and valid_after_dedup will "
          "often coincide (as they do on your real data, both 5,184) — this isn't a "
          "coincidence, it's because dedup here mostly just resolves retry-superseded "
          "failures rather than removing valid rows, per the breakdown above. State N "
          "as one number (5,184 on your data) with the mechanism, not '5,184 before / "
          "5,156 after' — the 5,156 figure comes from treating the 28 duplicates and "
          "the 44 errors as disjoint, which they are not.")

    # Grid completeness ------------------------------------------------------
    print("\n" + "=" * 78)
    print("GRID COMPLETENESS")
    print("=" * 78)
    gens_per_mt = (valid.groupby(["generator", "topic"])["gen_index"]
                   .nunique().rename("n_gens"))
    bad_g = gens_per_mt[gens_per_mt != 5]
    print(f"(model, topic) cells with != 5 generations: {len(bad_g)}"
          + ("" if bad_g.empty else f"\n{bad_g.to_string()}"))

    judges_per_gen = (valid.groupby(["generator", "topic", "gen_index"])["judge"]
                      .nunique().rename("n_judges"))
    dist = judges_per_gen.value_counts().sort_index()
    print(f"\njudges per generation (after error drop):\n{dist.to_string()}")
    print(f"generations total: {judges_per_gen.shape[0]} (expected 1,040)")

    # Family disjointness ----------------------------------------------------
    print("\n" + "=" * 78)
    print("FAMILY-DISJOINTNESS (post-filter confirmation)")
    print("=" * 78)
    print("Same-family rows are now dropped inside load_judgments() itself, so this")
    print("must always read 0 here — it's a confirmation the filter ran, not the")
    print("primary defense (see 'same-family, non-error rows dropped' above for how")
    print("many real verdicts that filter actually removed).")
    v = valid.copy()
    v["gen_family"] = v["generator"].map(bw.family_of)
    v["judge_family"] = v["judge"].map(bw.family_of)
    viol = v[v["gen_family"] == v["judge_family"]]
    print(f"same-family (generator, judge) verdicts: {len(viol)} (must be 0)")
    if len(viol):
        print("UNEXPECTED — the construction-time filter should make this impossible;")
        print("re-check family_of()'s keyword table against the families below.")
        print(viol.groupby(["generator", "judge"]).size().to_string())

    panel = (v.groupby("generator")["judge"]
             .agg(lambda s: sorted(set(map(str, s)))).rename("judges"))
    print("\npanel per generator (should be 5 judges each, family-disjoint):")
    for gname, judges in panel.items():
        print(f"  {str(gname):40s} n={len(judges)}  {judges}")

    unknown = sorted({f for f in v["gen_family"].unique()
                      if str(f).startswith("unknown")} |
                     {f for f in v["judge_family"].unique()
                      if str(f).startswith("unknown")})
    if unknown:
        print(f"\nWARNING: unrecognised families {unknown} — extend "
              f"_FAMILY_KEYWORDS in bw_common.py so the check is meaningful.")


if __name__ == "__main__":
    main()
