"""Reproduce the supervisor-revision tables and exploratory sensitivity analyses.

Run from the repository root: .venv/bin/python paper/supervisor_revision/recalculate.py
Reads saved results; does not generate perspectives, call judges, or alter old results.
"""
from pathlib import Path
from itertools import product, combinations
import json
import os
import warnings

os.environ.setdefault("MPLCONFIGDIR", "/tmp/bweird-supervisor-matplotlib")
os.environ.setdefault("XDG_CACHE_HOME", "/tmp/bweird-supervisor-cache")
import numpy as np
import pandas as pd
from scipy.stats import rankdata
import statsmodels.formula.api as smf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
configs = json.loads((ROOT / "config/models.json").read_text())
models = [m["slug"] for m in configs]
names = {m["slug"]: m["display_name"].replace(" Preview", "") for m in configs}
# Preserve Table 2's original tiers. The middle tier is NOT a verified openness label.
tiers = dict(zip(models, ["Frontier"] * 4 + ["Strong/open-weight (original tier)"] * 7 + ["Small"] * 2))
origins = {m["slug"]: ("China" if m["family"] in {"deepseek", "alibaba", "moonshot", "z.ai"}
                         else "France" if m["family"] == "mistral" else "US") for m in configs}
# Access categories for the revision; Qwen Max is an official commercial API flagship.
categories = {m: ("Frontier/API" if i < 4 or m.startswith("qwen/") else
                  "Small open-weight" if i >= 11 else "Open-weight") for i, m in enumerate(models)}


def signed_rank(values):
    """Exact midrank sign enumeration; rounding removes CSV representation noise."""
    d = np.round(np.asarray(values, float), 12)
    d = d[d != 0]
    if not len(d):
        return {"n_nonzero": 0, "p_greater": 1., "p_two_sided": 1.}
    r = rankdata(np.abs(d))
    observed = r[d > 0].sum()
    null = np.asarray(list(product([0, 1], repeat=len(d)))) @ r
    upper, lower = (null >= observed).mean(), (null <= observed).mean()
    return {"n_nonzero": len(d), "w_positive": float(observed),
            "p_greater": float(upper), "p_two_sided": float(min(1, 2 * min(upper, lower)))}


def sign_flip(values):
    d = np.asarray(values, float)
    null = np.asarray(list(product([-1, 1], repeat=len(d)))) @ d / len(d)
    return float((np.abs(null) >= abs(d.mean()) - 1e-12).mean())


def bootstrap_pairs(values):
    values = np.asarray(values)
    idx = np.random.default_rng(42).integers(0, len(values), (10000, len(values)))
    return np.percentile(values[idx].mean(axis=1), [2.5, 97.5], axis=0)


topic = pd.read_csv(ROOT / "results/agg/prf_per_topic.csv")
assert not topic.duplicated(["generator", "topic_id"]).any()
assert len(topic) == 208 and topic.coverage_sum.between(0, 1).all()
topic["pair"] = topic.topic_id.str.extract(r"pair(\d+)").astype(int)
topic["arm"] = topic.topic_id.str.split("_").str[-1]
wide = topic.pivot(index="generator", columns=["arm", "pair"], values="coverage_sum").reindex(models)
W = wide["weird"].reindex(columns=range(1, 9)).to_numpy()
S = wide["serbian"].reindex(columns=range(1, 9)).to_numpy()
assert W.shape == S.shape == (13, 8) and np.isfinite(W + S).all()
D = W - S
ranking = pd.read_csv(ROOT / "results/agg/ranking.csv").set_index("generator").reindex(models)
assert np.allclose((W + S).mean(axis=1) / 2, ranking.coverage, rtol=0, atol=1e-12)
published = pd.read_csv(ROOT / "results/agg/weird_gap_summary.csv").iloc[0]
assert abs(D.mean() - published.mean_gap) < 1e-12
assert signed_rank(D.mean(axis=0))["p_greater"] == published.p_one_sided_weird_gt
# The original pipeline advances one shared RNG through 78 model comparisons first.
original_rng = np.random.default_rng(42)
for _ in range(78):
    original_rng.choice([-1., 1.], size=(10000, 16))
original_idx = original_rng.integers(0, 8, (10000, 8))
original_ci = np.percentile(D.mean(axis=0)[original_idx].mean(axis=1), [2.5, 97.5])
assert np.allclose(original_ci, [published.mean_ci_lo, published.mean_ci_hi])
# One independent known example catches rank/tie and duplicate-coverage mistakes.
assert signed_rank([1, 1])["p_greater"] == 0.25
example = np.array([[1, 2, 2, 4, 0], [1, 2, 2, 4, 0], [1, 2, 3, 4, 0],
                    [1, 2, 0, 0, 0], [1, 0, 0, 4, 0]])
assert np.isclose(np.mean([len(set(row) - {0}) / 5 for row in example]), .56)

rows = []
for i, m in enumerate(models):
    ci = bootstrap_pairs(np.column_stack([W[i], S[i]]))
    rows.append({"model": names[m], "slug": m, "original_tier": tiers[m], "revision_category": categories[m], "origin": origins[m],
                 "overall_recall": ranking.loc[m, "coverage"],
                 "original_overall_ci_lo": ranking.loc[m, "coverage_lo"],
                 "original_overall_ci_hi": ranking.loc[m, "coverage_hi"],
                 "weird_recall": W[i].mean(), "weird_ci_lo": ci[0, 0], "weird_ci_hi": ci[1, 0],
                 "serbian_recall": S[i].mean(), "serbian_ci_lo": ci[0, 1], "serbian_ci_hi": ci[1, 1],
                 "gap": D[i].mean()})
model_table = pd.DataFrame(rows)
model_table.to_csv(OUT / "model_recall.csv", index=False)
pd.DataFrame(D, index=[names[m] for m in models], columns=[f"pair{p:02d}" for p in range(1, 9)]).to_csv(OUT / "paired_differences_13x8.csv", index_label="model")

groups = {t: [i for i, m in enumerate(models) if tiers[m] == t] for t in dict.fromkeys(tiers.values())}
groups.update({o: [i for i, m in enumerate(models) if origins[m] == o] for o in ["US", "China", "France"]})
# Verified public-weight releases; Qwen Max is kept separate pending a release source.
groups["Open weights excluding Qwen Max"] = [i for i in range(4, 13) if "qwen/" not in models[i]]
group_rows = []
for g, idx in groups.items():
    w, s = W[idx].mean(axis=0), S[idx].mean(axis=0)
    group_rows.append({"group": g, "n_models": len(idx), "weird_recall": w.mean(),
                       "serbian_recall": s.mean(), "overall_recall": (w.mean() + s.mean()) / 2,
                       "gap": (w-s).mean()})
pd.DataFrame(group_rows).to_csv(OUT / "group_recall.csv", index=False)

access_groups = {g: [i for i,m in enumerate(models) if categories[m] == g]
                 for g in ["Frontier/API", "Open-weight", "Small open-weight"]}
assert [len(i) for i in access_groups.values()] == [5, 6, 2]
assert sorted(i for members in access_groups.values() for i in members) == list(range(13))
access_groups["All open-weight"] = access_groups["Open-weight"] + access_groups["Small open-weight"]
access_rows = []
for g, idx in access_groups.items():
    w,s = W[idx].mean(axis=0), S[idx].mean(axis=0)
    access_rows.append({"group":g, "n_models":len(idx), "weird_recall":w.mean(),
                       "serbian_recall":s.mean(), "overall_recall":(w+s).mean()/2, "gap":(w-s).mean()})
pd.DataFrame(access_rows).to_csv(OUT / "access_group_recall.csv", index=False)
access_tests = []
for a,b in list(combinations(list(access_groups)[:3],2)) + [("Frontier/API","All open-weight")]:
    ia,ib = access_groups[a],access_groups[b]
    diff=((W[ia]+S[ia])/2).mean(axis=0)-((W[ib]+S[ib])/2).mean(axis=0)
    ci=bootstrap_pairs(diff)
    access_tests.append({"contrast":a+" minus "+b,"recall_difference":diff.mean(),
                         "ci_lo":ci[0],"ci_hi":ci[1],"p_two_sided":sign_flip(diff)})
at=pd.DataFrame(access_tests)
ps=at.p_two_sided.to_numpy()
order=np.argsort(ps)
adjusted=np.empty(len(ps))
adjusted[order]=np.minimum(1,np.maximum.accumulate(ps[order]*np.arange(len(ps),0,-1)))
at["p_holm_4"]=adjusted
at.to_csv(OUT / "access_group_contrasts.csv",index=False)

contrasts = []
pairs = list(combinations(list(groups)[:3], 2)) + [("US", "China")]
for a, b in pairs:
    ia, ib = groups[a], groups[b]
    perf = ((W[ia]+S[ia])/2).mean(axis=0) - ((W[ib]+S[ib])/2).mean(axis=0)
    gap = D[ia].mean(axis=0) - D[ib].mean(axis=0)
    ci = bootstrap_pairs(np.column_stack([perf, gap]))
    contrasts.append({"contrast": a + " minus " + b, "recall_difference": perf.mean(),
                      "recall_ci_lo": ci[0, 0], "recall_ci_hi": ci[1, 0],
                      "recall_p_two_sided": sign_flip(perf), "gap_difference": gap.mean(),
                      "gap_ci_lo": ci[0, 1], "gap_ci_hi": ci[1, 1], "gap_p_two_sided": sign_flip(gap)})
ct = pd.DataFrame(contrasts)
# Holm across the three original-tier performance contrasts; RQ3's two contrasts separately.
for indexes in [[0, 1, 2], [3]]:
    if len(indexes) == 1:
        ps = np.array([ct.loc[3, "recall_p_two_sided"], ct.loc[3, "gap_p_two_sided"]])
    else:
        ps = ct.loc[indexes, "recall_p_two_sided"].to_numpy()
    order = np.argsort(ps)
    adjusted = np.empty(len(ps))
    adjusted[order] = np.minimum(1, np.maximum.accumulate(ps[order] * np.arange(len(ps), 0, -1)))
    if len(indexes) == 1:
        ct.loc[3, "recall_p_holm"] = adjusted[0]
        ct.loc[3, "gap_p_holm"] = adjusted[1]
    else:
        ct.loc[indexes, "recall_p_holm"] = adjusted
# Separate exploratory family: differences in cultural gaps among the original tiers.
ps = ct.loc[[0, 1, 2], "gap_p_two_sided"].to_numpy()
order = np.argsort(ps)
adjusted = np.empty(3)
adjusted[order] = np.minimum(1, np.maximum.accumulate(ps[order] * np.arange(3, 0, -1)))
ct.loc[[0, 1, 2], "gap_p_holm"] = adjusted
ct.to_csv(OUT / "exploratory_contrasts.csv", index=False)

rng = np.random.default_rng(42)
crossed = np.empty(10000)
crossed_data = D[np.argsort(models)]
for b in range(10000):
    mi = rng.integers(0, 13, 13)
    pi = rng.integers(0, 8, 8)
    crossed[b] = crossed_data[np.ix_(mi, pi)].mean()
frame = pd.DataFrame({"delta": D.ravel(), "model": np.repeat(models, 8),
                      "pair": np.tile(range(1, 9), 13), "one": 1})
with warnings.catch_warnings(record=True) as caught:
    fit = smf.mixedlm("delta ~ 1", frame, groups="one", re_formula="0",
                     vc_formula={"model": "0 + C(model)", "pair": "0 + C(pair)"}).fit(reml=True, method="lbfgs")
assert fit.converged
stats = {"primary": published.to_dict(), "model_mean_sensitivity": signed_rank(D.mean(axis=1)),
         "crossed_bootstrap_ci": np.percentile(crossed, [2.5, 97.5]).tolist(),
         "crossed_mixed_model": {"estimate": float(fit.fe_params.iloc[0]), "se": float(fit.bse_fe.iloc[0]),
              "p_two_sided": float(fit.pvalues.iloc[0]), "ci": fit.conf_int().iloc[0].tolist(),
              "variance_components": dict(zip(fit.model.exog_vc.names, fit.vcomp.tolist())),
              "residual_variance": float(fit.scale), "converged": bool(fit.converged),
              "warnings": [str(w.message) for w in caught]},
         "matrix_counts": {"positive": int((np.round(D,12)>0).sum()),
                           "negative": int((np.round(D,12)<0).sum()), "zero": int((np.round(D,12)==0).sum())}}
(OUT / "analysis_results.json").write_text(json.dumps(stats, indent=2) + "\n")

# A single figure preserves pairing at all three levels requested in the notes.
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
fig, axes = plt.subplots(1, 3, figsize=(15, 6), gridspec_kw={"width_ratios": [1, 1.35, 1]})
for ax, w, s, labels, title in [
    (axes[0], W.mean(axis=0), S.mean(axis=0), [f"Pair {p}" for p in range(1, 9)], "A. Eight topic-pair means"),
    (axes[1], W.mean(axis=1), S.mean(axis=1), [names[m] for m in models], "B. Thirteen model means")]:
    y = np.arange(len(labels))
    ax.hlines(y, np.minimum(w,s), np.maximum(w,s), color="#b4bdc5", lw=2)
    ax.scatter(w, y, color="#225e91", s=28, label="WEIRD", zorder=3)
    ax.scatter(s, y, color="#b95832", s=28, label="Serbian", zorder=3)
    ax.set(yticks=y, yticklabels=labels, xlim=(0,1), xlabel="Recall", title=title)
    ax.invert_yaxis()
    ax.grid(axis="x", alpha=.15)
axes[0].legend(loc="lower left", frameon=False)
axes[2].scatter(S.ravel(), W.ravel(), s=23, alpha=.6, color="#225e91", edgecolor="none")
axes[2].plot([0,1],[0,1],color="#7c8994",linestyle="--",lw=1)
axes[2].set(xlim=(0,1), ylim=(0,1), xlabel="Serbian recall", ylabel="WEIRD recall",
            title="C. All 104 matched cells")
axes[2].set_aspect("equal")
fig.suptitle("The same paired recalls, summarized at three levels", fontsize=15, y=1.02)
fig.text(.5, -.02, "Averages give equal weight to models and pairs. Panel C is descriptive: cells share models and topic pairs.", ha="center", fontsize=10)
fig.tight_layout(w_pad=2)
fig.savefig(OUT / "paired_recall.png", dpi=210, bbox_inches="tight")
plt.close(fig)
print(model_table[["model", "weird_recall", "serbian_recall", "gap"]].to_string(index=False))
print(ct.to_string(index=False))
print(json.dumps(stats, indent=2))
