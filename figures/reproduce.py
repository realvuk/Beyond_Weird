"""Reproduce both manuscript versions' charts from saved full-precision results.

Run `python figures/reproduce.py --help`. No API calls or analysis files are changed.
The first two charts adapt plot_1.py/plot_2.py; the three-panel chart adapts
paper/supervisor_revision/recalculate.py without running its other analyses.
"""

import argparse
import hashlib
import json
import os
import platform
import tempfile
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "bweird-figure-cache"))
os.environ.setdefault("XDG_CACHE_HOME", str(Path(tempfile.gettempdir()) / "bweird-figure-system-cache"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter

ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    "config/models.json", "data/topics.json", "results/agg/prf_per_topic.csv",
    "results/agg/ranking.csv", "results/agg/weird_gap_pair_deltas.csv",
    "results/agg/weird_gap_per_model.csv", "results/agg/weird_gap_summary.csv",
]
PAIR_LABELS = [
    "Confederate monuments / Partisans-Chetniks", "Catalan independence / Kosovo",
    "UK fracking / Jadar lithium", "Polish Catholic / Serbian Orthodox Church",
    "Canada residential schools / Srebrenica", "German immigration / Serbian migration route",
    "Orbán / Vučić", "Brexit / Serbia's West-Russia alignment",
]
SHORT_LABELS = [
    "Confederate monuments / Partisans", "Catalonia / Kosovo", "UK fracking / Jadar",
    "Polish Church / Serbian Church", "Residential schools / Srebrenica",
    "Germany immigration / Balkan route", "Orbán / Vučić", "Brexit / West-vs-Russia",
]
BLUE, ORANGE = "#2b5ecb", "#be621d"


def load_results(root=ROOT):
    """Validate the 13 x 8 matched design and reconcile all plotted summaries."""
    configs = json.loads((root / SOURCES[0]).read_text())
    models = [m["slug"] for m in configs]
    names = [m["display_name"].replace(" Preview", "") for m in configs]
    topics = pd.DataFrame(json.loads((root / SOURCES[1]).read_text()))
    cells = pd.read_csv(root / SOURCES[2])
    expected_topics = {f"pair{p:02d}_{a}" for p in range(1, 9) for a in ("weird", "serbian")}
    if (len(models) != 13 or len(set(models)) != 13 or len(topics) != 16
            or set(topics.topic_id) != expected_topics or len(cells) != 208
            or set(cells.generator) != set(models) or set(cells.topic_id) != expected_topics
            or cells.duplicated(["generator", "topic_id"]).any()):
        raise ValueError("Expected exactly 13 models x 16 unique topics (eight complete pairs).")
    for row in topics.itertuples():
        if row.topic_id != f"pair{row.pair_id:02d}_{row.arm}":
            raise ValueError(f"Topic metadata disagrees with its ID: {row.topic_id}")
    if not cells.coverage_sum.between(0, 1).all() or not cells.n_golds.eq(5).all():
        raise ValueError("Each topic must have five references and finite recall in [0, 1].")
    wide = cells.pivot(index="generator", columns="topic_id", values="coverage_sum").reindex(models)
    w, s = [wide[[f"pair{p:02d}_{arm}" for p in range(1, 9)]].to_numpy()
            for arm in ("weird", "serbian")]
    gaps = w - s
    ranking = pd.read_csv(root / SOURCES[3]).set_index("generator").reindex(models)
    pairs = pd.read_csv(root / SOURCES[4]).set_index("pair_id").reindex(range(1, 9))
    per_model = pd.read_csv(root / SOURCES[5]).set_index("generator").reindex(models)
    summary_rows = pd.read_csv(root / SOURCES[6])
    pooled = summary_rows.loc[summary_rows.analysis.eq("pooled_coverage")]
    if len(pooled) != 1:
        raise ValueError("Expected one pooled_coverage summary row.")
    pooled = pooled.iloc[0]
    if pooled.n_pairs != 8 or not per_model.n_pairs.eq(8).all():
        raise ValueError("All cultural comparisons must use the same eight matched pairs.")
    for observed, expected in [
        ((w + s).mean(axis=1) / 2, ranking.coverage),
        (gaps.mean(axis=0), pairs.mean_delta),
        (gaps.mean(axis=1), per_model.mean_gap),
        (gaps.mean(), pooled.mean_gap),
    ]:
        np.testing.assert_allclose(observed, expected, rtol=0, atol=1e-12)
    if not np.isfinite(per_model.p_bh).all() or not per_model.p_bh.between(0, 1).all():
        raise ValueError("Missing or invalid model-level adjusted p-values.")
    # Reproduce the historical RNG stream, not a fresh bootstrap with another CI.
    # Stage 6 sampled 78 model comparisons before drawing the 10,000 pair resamples.
    rng = np.random.default_rng(42)
    for _ in range(78):
        rng.choice([-1.0, 1.0], size=(10000, 16))
    indices = rng.integers(0, 8, size=(10000, 8))
    ci = np.percentile(gaps.mean(axis=0)[indices].mean(axis=1), [2.5, 97.5])
    np.testing.assert_allclose(ci, [pooled.mean_ci_lo, pooled.mean_ci_hi], rtol=0, atol=1e-12)
    return names, w, s, pooled, per_model


def plot_model_gap(names, w, s, pooled, per_model):
    """Original paper Figure 1: model means and a pooled pair-bootstrap interval."""
    gap = (w - s).mean(axis=1)
    # Round only for sorting so tied means retain the configuration order.
    order = np.argsort(-np.round(gap, 12), kind="stable")[::-1]
    fig, ax = plt.subplots(figsize=(11, 7.5))
    for y, i in enumerate(order):
        color = ORANGE if gap[i] > 0 else BLUE
        ax.plot([0, gap[i]], [y, y], color=color, alpha=.45, lw=2)
        ax.scatter(gap[i], y, color=color, s=70, zorder=3)
    ax.set_yticks(range(13), [names[i] for i in order])
    ax.axvline(0, color=".6", lw=1)
    ax.axhline(-.8, color=".6", ls="--", lw=1)
    mean, lo, hi = pooled[["mean_gap", "mean_ci_lo", "mean_ci_hi"]]
    ax.errorbar(mean, -2.2, xerr=[[mean - lo], [hi - mean]], fmt="D", color="black",
                capsize=6, lw=2, markersize=7)
    ax.text(.063, -2.05, f"pooled  {mean:.3f}", va="bottom")
    ax.text(.063, -2.55, f"95% CI  {lo:.3f} to {hi:.3f}", va="top")
    ax.text(-.02, 13.5, f"covers Serbian arm more fully (n = {(gap < 0).sum()})",
            color=BLUE, ha="right")
    ax.text(.02, 13.5, f"covers WEIRD arm more fully (n = {(gap > 0).sum()})", color=ORANGE)
    title = "The thirteen models split in sign"
    if not per_model.p_bh.lt(.05).any():
        title += "; no gap survives correction"
    ax.set(title=title, xlabel="Mean coverage gap (WEIRD - Serbian)",
           xlim=(-.15, .20), ylim=(-3.2, 14.2))
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    fig.tight_layout()
    return fig


def plot_topic_slopes(names, w, s, pooled, per_model):
    """Original paper Figure 2, retaining the original slope-chart geometry."""
    w, s = w.mean(axis=0), s.mean(axis=0)
    gap = w - s
    fig, ax = plt.subplots(figsize=(11, 6.5))
    colors = [ORANGE if d > 0 else BLUE for d in gap]
    for i in range(8):
        ax.plot([0, 1], [w[i], s[i]], color=colors[i], lw=2, marker="o", markersize=6)
    ax.plot([0, 1], [w.mean(), s.mean()], color="black", lw=3.5, marker="s", markersize=7)
    ax.text(.02, w.mean() + .006, "arm mean", ha="left", va="bottom")
    # Deliberate label positions from the original figure, for these eight topics.
    for i, target_y in zip(np.argsort(-s), [.698, .679, .660, .641, .622, .603, .468, .449], strict=True):
        ax.plot([1, 1.03, 1.03, 1.08], [s[i], s[i], target_y, target_y], color=colors[i], lw=.8)
        ax.text(1.10, target_y, f"{SHORT_LABELS[i]}  ({100 * gap[i]:+.1f})",
                color=colors[i], va="center", fontsize=10)
    ax.set_xticks([0, 1], [f"WEIRD topic\n(mean {w.mean():.3f})",
                           f"Serbian topic\n(mean {s.mean():.3f})"])
    ax.set(xlim=(-.2, 1.8), ylim=(.435, .715),
           ylabel="Mean coverage across the thirteen models")
    ax.set_title(f"Matched topic pairs: {(gap > 0).sum()} favour WEIRD and {(gap < 0).sum()} favour Serbian",
                 loc="left", pad=15)
    fig.text(.5, .005, "Parentheses: WEIRD - Serbian difference in percentage points.",
             ha="center", fontsize=9)
    fig.tight_layout(rect=(0, .025, 1, 1))
    return fig


def plot_pair_gaps(names, w, s, pooled, per_model):
    """Revised paper Figure 1: eight pair means, with the primary t-based interval."""
    gap = (w - s).mean(axis=0) * 100
    fig, ax = plt.subplots(figsize=(11, 7))
    y = np.arange(8)
    ax.hlines(y, 0, gap, color="#b6c5d1", lw=1.7)
    ax.scatter(gap, y, color="#2b6084", s=36, zorder=3)
    for i, value in enumerate(gap):
        ax.annotate(f"{value:+.1f}", (value, i), xytext=(5 if value >= 0 else -5, 0),
                    textcoords="offset points", ha="left" if value >= 0 else "right", va="center")
    mean, lo, hi = pooled[["mean_gap", "mean_t_lo", "mean_t_hi"]] * 100
    ax.errorbar(mean, 9, xerr=[[mean - lo], [hi - mean]], fmt="D", color="#222222", capsize=5)
    ax.set_yticks(list(y) + [9], PAIR_LABELS + ["Mean across eight pairs"])
    ax.get_yticklabels()[-1].set_fontweight("bold")
    ax.text(0, 9.8, f"{mean:+.1f} pp (95% CI: {lo:+.1f} to {hi:+.1f})", ha="center")
    ax.text(-21, -.8, "Favours Serbian", ha="left")
    ax.text(21, -.8, "Favours WEIRD", ha="right")
    ax.axvline(0, color=".5", lw=1)
    ax.axhline(8.25, color=".8", lw=1)
    ax.set(xlim=(-24, 24), ylim=(10.4, -1.4),
           xlabel="Recall gap (WEIRD - Serbian), percentage points")
    ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:+g}" if value else "0"))
    ax.grid(axis="x", color=".9")
    ax.set_axisbelow(True)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0, pad=10)
    fig.suptitle("Recall differences across eight matched topic pairs", fontsize=15, fontweight="bold")
    fig.text(.5, .91, "Each topic-pair point averages the 13 generators. Topic names follow Table 1.",
             ha="center", fontsize=10)
    fig.text(.5, .015, "95% t-based interval for the mean; pair-specific intervals are not shown.",
             ha="center", fontsize=9)
    fig.tight_layout(rect=(0, .04, 1, .90))
    return fig


def plot_paired_recall(names, w, s, pooled, per_model):
    """Revised paper Figure 2: the existing three-panel figure, without reanalysis."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 6), gridspec_kw={"width_ratios": [1, 1.35, 1]})
    for ax, wa, sa, labels, title in [
        (axes[0], w.mean(axis=0), s.mean(axis=0), [f"Pair {p}" for p in range(1, 9)], "A. Eight topic-pair means"),
        (axes[1], w.mean(axis=1), s.mean(axis=1), names, "B. Thirteen model means"),
    ]:
        y = np.arange(len(labels))
        ax.hlines(y, np.minimum(wa, sa), np.maximum(wa, sa), color="#b4bdc5", lw=2)
        ax.scatter(wa, y, color="#225e91", s=28, label="WEIRD", zorder=3)
        ax.scatter(sa, y, color="#b95832", s=28, label="Serbian", zorder=3)
        ax.set(yticks=y, yticklabels=labels, xlim=(0, 1), xlabel="Recall", title=title)
        ax.invert_yaxis()
        ax.grid(axis="x", alpha=.15)
    axes[0].legend(loc="lower left", frameon=False)
    axes[2].scatter(s.ravel(), w.ravel(), s=23, alpha=.6, color="#225e91", edgecolor="none")
    axes[2].plot([0, 1], [0, 1], color="#7c8994", ls="--", lw=1)
    axes[2].set(xlim=(0, 1), ylim=(0, 1), xlabel="Serbian recall", ylabel="WEIRD recall",
                title="C. All 104 matched cells")
    axes[2].set_aspect("equal")
    fig.suptitle("The same paired recalls, summarized at three levels", fontsize=15, y=1.02)
    fig.text(.5, -.02, "Averages give equal weight to models and pairs. Panel C is descriptive: cells share models and topic pairs.",
             ha="center", fontsize=10)
    fig.tight_layout(w_pad=2)
    return fig


PLOTS = {
    "per_model_coverage_gap": plot_model_gap,
    "coverage_by_topic_slopechart": plot_topic_slopes,
    "primary_pair_gaps": plot_pair_gaps,
    "paired_recall": plot_paired_recall,
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--figure", choices=["all", *PLOTS], default="all")
    parser.add_argument("--out-dir", type=Path, default=ROOT / "output/pdf/paper_figures")
    parser.add_argument("--check-only", action="store_true", help="validate data and reproduce the saved bootstrap CI without drawing")
    args = parser.parse_args()
    data = load_results()
    print("PASS: 208 model-topic scores; 104 pairs; model, pair and pooled means; historical bootstrap CI.")
    if args.check_only:
        return
    args.out_dir.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "pdf.fonttype": 42, "ps.fonttype": 42})
    selected = PLOTS if args.figure == "all" else {args.figure: PLOTS[args.figure]}
    for name, plot in selected.items():
        fig = plot(*data)
        for suffix in ("pdf", "png"):
            path = args.out_dir / f"{name}.{suffix}"
            metadata = {"CreationDate": None, "ModDate": None} if suffix == "pdf" else None
            fig.savefig(path, dpi=300, bbox_inches="tight", metadata=metadata)
            print(path.resolve())
        plt.close(fig)
    manifest = {"figures": list(selected), "python": platform.python_version(),
                "matplotlib": matplotlib.__version__, "numpy": np.__version__, "pandas": pd.__version__,
                "source_sha256": {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in SOURCES}}
    (args.out_dir / "reproduction.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
