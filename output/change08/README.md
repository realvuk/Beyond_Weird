# Change 08: replacement figure

The replacement figure is ready. The eight topic-pair points and mean are unchanged; the mean's error bar now shows the saved 95% t-based confidence interval: **−10.3 to +7.7 percentage points**. Its footer identifies the interval correctly.

## Use it in your paper

1. Replace `plots/primary_pair_gaps.png` in your LaTeX project with [this PNG](/Users/vuk/Downloads/BWEIRD/output/change08/primary_pair_gaps.png). Keep the filename and `plots` folder unchanged. In Overleaf, upload it into `plots` and replace the old file.
2. Replace the whole figure block, originally lines 409–414 of `0_version_2.tex`, with the following. If earlier edits have moved the lines, search for `\label{fig:paired-recall}`.

```latex
\begin{figure*}[!t]
\centering
\includegraphics[width=\textwidth]{plots/primary_pair_gaps.png}
\caption{Recall differences for the eight matched topic pairs. Each point is the WEIRD-minus-Serbian difference averaged over the $13$ generators; positive values favour WEIRD topics. The diamond shows the mean across pairs, with the $95\%$ $t$-based confidence interval used in the primary analysis. Pair-specific confidence intervals are not shown.}
\label{fig:paired-recall}
\end{figure*}
```

Use one backslash in `\%`, as shown above. Recompile the paper after replacing both the image and caption.

An equivalent [vector PDF](/Users/vuk/Downloads/BWEIRD/output/change08/primary_pair_gaps.pdf) is also available. To use it, upload it into `plots` and change only `.png` to `.pdf` in the `\includegraphics` line. Either file shows the same result.

The original manuscript and figure under `Vuk_First_Journal_Paper` have not been overwritten.

## Reproduction

The existing [plotting script](/Users/vuk/Downloads/BWEIRD/figures/reproduce.py) now reads `mean_t_lo` and `mean_t_hi` from the `pooled_coverage` row of [the saved summary](/Users/vuk/Downloads/BWEIRD/results/agg/weird_gap_summary.csv). It does not rerun the experiment or replace the topic scores. The original per-model figure retains its historical bootstrap interval.

From `/Users/vuk/Downloads/BWEIRD`:

```sh
.venv/bin/python figures/reproduce.py --figure primary_pair_gaps --out-dir output/change08
.venv/bin/python figures/check_reproduction.py
```
