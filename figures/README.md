# Reproduce the paper's charts

From the BWEIRD folder, using the existing environment:

```bash
.venv/bin/python figures/reproduce.py
```

In the full repository, `make figures` runs the same command. It creates four
charts, each as a vector PDF and a 300-dpi PNG, in `output/pdf/paper_figures/`.
It runs without a display, API key, or network access. Inputs and existing paper
figures are not overwritten. Re-running replaces only these generated outputs.

On another computer, or after extracting the portable ZIP, install the three
plotting dependencies once (Python 3.12 or newer):

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r figures/requirements.txt
.venv/bin/python figures/reproduce.py
```

On Windows use `.venv\Scripts\python.exe` instead of `.venv/bin/python`.
The ZIP includes the required saved inputs, scripts, and generated charts; it
does not require the full evaluation project. `make` is optional and is not
needed for the ZIP. The script resolves inputs relative to itself, so it also
works when called by absolute path from another working directory.

## Which output belongs to which paper?

| Paper | Figure | Output stem / `--figure` argument |
|---|---|---|
| `paper/Final_Full_Paper.pdf` | 1: per-model WEIRD-Serbian coverage gap | `per_model_coverage_gap` |
| `paper/Final_Full_Paper.pdf` | 2: paired topic coverage slope chart | `coverage_by_topic_slopechart` |
| `output/pdf/readability_revision/revised_paper.pdf` | 1: primary gaps across eight topic pairs | `primary_pair_gaps` |
| Revised paper, Appendix E; also supervisor revision | 2: paired recall at topic, model, and model-pair levels | `paired_recall` |

Generate one figure, or choose a destination:

```bash
.venv/bin/python figures/reproduce.py --figure primary_pair_gaps
.venv/bin/python figures/reproduce.py --out-dir /tmp/bweird-charts
```

Use the generated PDF for LaTeX or print and the PNG for slides or Word. The
revised manuscript already uses the names `primary_pair_gaps.pdf` and
`paired_recall.png`; copy those two generated files into your Overleaf project
if you want to replace its figure assets.

## Data and calculations

`reproduce.py` uses full-precision saved scores, not values transcribed from the
PDF. `coverage_sum` is the manuscript's recall/coverage measure.

| Input | Purpose |
|---|---|
| `config/models.json` | Stable generator IDs, display names, and panel order |
| `data/topics.json` | Check the eight WEIRD-Serbian pair identities |
| `results/agg/prf_per_topic.csv` | The 208 model-topic scores underlying every plotted point |
| `results/agg/ranking.csv` | Cross-check each model's overall mean |
| `results/agg/weird_gap_pair_deltas.csv` | Cross-check the eight mean pair gaps |
| `results/agg/weird_gap_per_model.csv` | Cross-check the thirteen mean model gaps and read adjusted p-values |
| `results/agg/weird_gap_summary.csv` | Saved pooled estimate, t interval and historical pair-bootstrap interval |

For each model and pair, the gap is **WEIRD minus Serbian**. A pair point
averages 13 models; a model point averages eight pairs. The pooled estimate
averages the eight pair means. Multiplying a gap by 100 gives percentage points.
The slope chart's coordinates and the three-panel chart use recall on a 0-1
scale. The original per-model plot also uses a fractional gap; the revised
primary plot uses percentage points.

The primary topic-pair plot (`primary_pair_gaps`) uses the saved **95% t-based
interval across eight pair means**, with seven degrees of freedom: columns
`mean_t_lo` and `mean_t_hi`, approximately `[-0.10291829, 0.07676444]` in recall
units, displayed as `[-10.3, +7.7]` percentage points. Its mean and eight topic
points are unchanged. The original per-model plot retains its historical
bootstrap interval.

That historical pooled interval resamples **eight topic pairs**, keeping all 13 models
together within a pair. It is not an interval for individual model or pair
points. The script independently recreates the saved 10,000-resample percentile
interval: the original analysis seeded NumPy with 42, then drew the random signs
for 78 model comparisons before drawing the pair-bootstrap indices. Starting
a fresh seed-42 bootstrap without advancing that stream produces a slightly
different Monte Carlo interval. The reproduced endpoints are approximately
`[-0.08096154, 0.05822596]`, around the mean `-0.01307692`.

The script checks complete pairs, duplicate/missing cells, finite recall within
[0, 1], five references per topic, all saved means, and the historical interval
before exporting. It does not rerun generation, judging, or change the analysis.
`reproduction.json` records input SHA-256 hashes and the runtime versions used.

## Fidelity and editing

The original `plot_1.py` (slope chart) and `plot_2.py` (model-gap chart), plus
their rounded CSV inputs, remain available. Their numbering is the reverse of
the figure numbering in `Final_Full_Paper.pdf`. They produce PNGs and open an
interactive plot window when run directly.

The new script adapts those plots and the existing three-panel plotting code in
`paper/supervisor_revision/recalculate.py`. It recreates the revised primary
gap plot from its saved data. The same comparisons and numerical findings are
preserved; these are not pixel-identical exports. Differences include using
full-precision coordinates, full model names, dynamically calculated numeric
labels, small spacing changes, and an explicit units note on the slope chart.
Unrelated older p-value/effect-size columns in the rounded figure CSV are not
used by the new script.

Edit the four `plot_*` functions in `reproduce.py` to change sizes, colours,
titles, or typography. `PAIR_LABELS` and `SHORT_LABELS` control the topic labels.
The topic set, 13-model design, and slope-label positions are deliberately
specific to this paper; this is not a general plotting library.

## Checks

```bash
.venv/bin/python figures/reproduce.py --check-only
.venv/bin/python figures/check_reproduction.py
```

The second command additionally checks known paper values, invariance to shuffled
CSV rows, rejection of missing/duplicate/NaN cells, and rejection of an incorrect
pooled confidence interval. It modifies only temporary copies of the inputs.

Tested with Python 3.14.3, Matplotlib 3.11.1, NumPy 2.5.1, and pandas 3.0.3.
Numeric checks and visual inspection passed for all four exported charts.
Font rendering can vary slightly across platforms or package versions.
