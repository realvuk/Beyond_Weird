# Statistical simplification: proposed manuscript revisions

Prepared 2 October 2026. This is a replacement-text guide, not an edited manuscript.

**Source:** [0_version_2.tex](/Users/vuk/Downloads/Vuk_First_Journal_Paper/0_version_2.tex), 1,101 lines.

**Source SHA-256:** `840867fdd0c582c325a1f4f8bb59d3f019b2d0a57aecd2f3d260c4d6c4e263c1`

All line ranges below refer to this original source, before any edits. Each change includes a clickable location and a searchable anchor. Apply replacements from the bottom of the file upwards, or locate them by their anchors after earlier edits change the line numbers. Only copy the contents of the LaTeX code blocks into the manuscript.

**PDF locations:** No PDF accompanies this exact source in the supplied `Vuk_First_Journal_Paper` folder. Page numbers from older PDFs would not be reliable, so this guide uses verified LaTeX locations throughout. These are source-file lines, not the margin line numbers in a compiled submission PDF.

## 1. Scope and recommended decisions

The aim is to make the study easier to follow while preserving the completed experiment, reported scores, three research questions, corrections attached to retained tests, and qualifications on the conclusions. This guide drafts reporting and presentation changes; it does not rerun analyses or alter the source manuscript.

The legible notes in the supervisor's photograph emphasise the progression from individual judge assignments to a model-topic score, followed by the WEIRD/Serbian, model-category, and US/China comparisons. Some handwriting is faint. The photograph does not visibly prescribe the full collection of statistical methods now reported. The unrelated website-maintenance notes at the top are not part of this revision brief.

### Recommended reporting structure

| Component | Main paper | Supplement / appendix |
|---|---|---|
| Scoring | Recall, with the concrete five-assignment example and the three aggregation steps | Exact duplicate-credit and missing-judgment equations; precision and F1 |
| RQ1 | Eight matched-pair differences; mean gap; one 95% t-based interval; one primary Wilcoxon result | Two-sided result, rank-biserial effect size, bootstrap interval, upper bound, power illustration and model-based checks |
| RQ2 | Descriptive model recall table; category means; concise adjusted results for the defined category family | All four category tests, model-level intervals, all 78 pairwise model tests and their sensitivity analysis |
| RQ3 | Selected-group means, effect sizes, intervals and adjusted results for the two outcomes | Raw p-values and calculation details; preserve the model-composition caveat in the main paper |
| Judge checks | Nominal Krippendorff's alpha, no-match rates, brief leave-one-judge-out summary | Fleiss' kappa, Gwet's AC1, pairwise judge agreement and detailed removal results |
| Multiple comparisons | Define Holm adjustment once for the limited exploratory comparison families | Retain Benjamini-Hochberg with the 78 pairwise and 13 per-model test families |

This is a reduction in the main paper's statistical burden, not a deletion of the analysis record. Benjamini-Hochberg and Holm protect different error rates; they are not interchangeable names for the same correction. Retain each correction with the tests for which it was used. [R documentation on p-value adjustments](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/p.adjust.html)

Use alpha as the single main agreement coefficient because it supports multiple raters and incomplete ratings. The manuscript already reports alpha, so this recommendation does not introduce a new calculation. [Krippendorff's methodological description](https://www.asc.upenn.edu/sites/default/files/2021-03/Computing%20Krippendorff%27s%20Alpha-Reliability.pdf)

### Two qualifications that remain necessary

1. **Direction of the primary test.** The default replacements retain the manuscript's one-sided test. That is appropriate if the directional hypothesis and test choice preceded inspection of the results. The source does not establish that history, and this guide does not assert preregistration or invent it. Section 5 gives coordinated alternative wording if the two-sided test should be primary. Do not choose between them on the basis of which p-value is preferable. Wilcoxon requires independent differences and a symmetry assumption under the null. [SciPy documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.wilcoxon.html)
2. **Interpretation of the interval.** The t interval estimates the arithmetic mean gap; it is not an interval obtained by inverting the Wilcoxon test. Its small-sample interpretation assumes independent, approximately normally distributed pair-level differences. Keeping that qualification is especially important with eight investigator-selected topic pairs. [NIST confidence-interval guidance](https://www.itl.nist.gov/div898/handbook/eda/section3/eda352.htm)

The draft retains the existing bootstrap intervals for the secondary US/China contrasts. Changing those to t intervals would require a further analytical decision and recalculation. “One primary interval” below means one interval for the primary RQ1 estimate, not relabelling every existing interval in the paper.

## 2. Change map

| Change | Original LaTeX lines | Action |
|---|---:|---|
| 01 | 166 | Simplify abstract; remove repeated test name and agreement coefficient |
| 02 | 190–192 | Keep recall and the main finding; remove per-model testing from introduction |
| 03 | 291 | Give a short generation-to-comparison overview |
| 04 | 333 | Explicitly distinguish one assignment from the five assignments used for scoring |
| 05 | 343–370 | Preserve and clarify the three scoring steps |
| 06 | 372–396 | Replace the statistical-methods subsection with a shorter RQ-led explanation |
| 07 | 401–407 | Report one primary interval and one primary test result |
| 08 | 412; image at 411 | Align the main figure with the primary t interval; asset update required |
| 09 | 418 | Remove the exhaustive pairwise-testing narrative from RQ2 |
| 10 | 420–449 | Show descriptive model recall without repeating supplementary intervals |
| 11 | 451 | Simplify category results; retain adjusted inference |
| 12 | 453 | Keep within-category variation and panel-composition limitations |
| 13 | 457–458 | State the overall US/China result once |
| 14 | 476–478 | State the cultural-gap result once and preserve composition caveats |
| 15 | 480–500 | Use one main agreement coefficient and retain the judge-removal check |
| 16 | 509 | Remove dependence of the discussion on the per-model testing battery |
| 17 | 519 | Replace broad category language with a precise description |
| 18 | 541 | Calibrate what judge consistency can establish |
| 19 | 545 | Shorten the statistical-resolution limitation |
| 20 | 783–787 | Clearly separate primary interval from supplementary calculations |
| 21 | 813 | Clarify the primary and supplementary signed-rank outputs |
| 22 | 832–834 | Preserve category-test details and results removed from main text |
| 23 | 840 | Preserve the two developer-group tests and their raw/adjusted outputs |
| 24 | 905 | Clarify the role of supplementary model intervals and precision/F1 |
| 25 | 934 | Preserve both pairwise-testing results and their conflicting sensitivity |
| 26 | 978–985 | Move the three-coefficient agreement table into the appendix |

No changes are proposed to the research questions at lines 181–188, topic selection, reference construction, prompts, panel membership, model categories, execution records, or the empirical conclusion at line 565. Keep the equations and execution details at lines 722–778, including the missing-data adjustment.

## 3. Main-paper replacement text

### Change 01 — Abstract

**Replace original lines 166–166.** [Open location](/Users/vuk/Downloads/Vuk_First_Journal_Paper/0_version_2.tex:166)

Anchor: `Large language models can describe political controversies accurately`

Purpose: lead with the study and result. Identify the test in the methods, and give the agreement statistic in the judge-check subsection. The observed result and uncertainty remain unchanged.

```latex
Large language models can describe political controversies accurately while omitting relevant perspectives. We test whether they recover fewer documented perspectives on Serbian controversies than on structurally matched topics from Western, Educated, Industrialised, Rich, and Democratic (WEIRD) settings. The benchmark pairs eight Serbian controversies with WEIRD counterparts. Each of the 16 topics has five reference perspectives documented in surveys, polling, referendum results, research, or public debate. Thirteen LLMs each generated five perspectives per topic in English, and five LLM judges from other developers matched each output to a reference or returned no match. Mean recall was $0.581$ on WEIRD topics and $0.594$ on Serbian topics. The mean WEIRD-minus-Serbian difference across the eight pairs was $-1.3$ percentage points ($95\%$ CI: $-10.3$ to $7.7$), with no evidence for the hypothesised WEIRD advantage ($p=0.680$). Differences between individual pairs ($-16.9$ to $+19.1$ points) were much larger than the pooled difference. Inter-judge agreement was similar across the two settings, although agreement does not establish accuracy. Coverage was incomplete in both settings, and the result does not establish equivalent coverage.
```

### Change 02 — Introduction: outcome and finding

**Replace original lines 190–192.** [Open location](/Users/vuk/Downloads/Vuk_First_Journal_Paper/0_version_2.tex:190)

Anchor: `Recall is the principal outcome because all three questions`

Purpose: preserve the hierarchy of research questions without introducing the 13 per-model tests or their correction before the methods.

```latex
Recall is the principal outcome because all three questions concern recovery of documented perspectives. Precision and F1 provide supplementary descriptions of matching behaviour. The category and developer-country comparisons are exploratory; the model categories describe access and relative size, not a capability ranking.

We do not detect the predicted WEIRD advantage. Mean recall is $0.581$ for WEIRD topics and $0.594$ for Serbian topics, with four matched pairs favouring each side. Coverage nevertheless remains incomplete. Even the highest-recall model misses roughly three of every ten reference perspectives on average.
```

### Change 03 — Evaluation overview

**Replace original lines 291–291.** [Open location](/Users/vuk/Downloads/Vuk_First_Journal_Paper/0_version_2.tex:291)

Anchor: `The procedure separates generation, judging, and scoring.`

```latex
The evaluation proceeds in four stages. First, each model generates perspectives for a topic without seeing the references. Second, five judges independently match each generated perspective to a reference or return no match. Third, we calculate recall from these assignments for each model and topic. Finally, we use the model-topic scores to describe model performance and compare the matched cultural settings, model categories, and developer groups.
```

### Change 04 — Explain what an individual judge does

**Replace original lines 333–333.** [Open location](/Users/vuk/Downloads/Vuk_First_Journal_Paper/0_version_2.tex:333)

Anchor: `Each of five LLM judges receives one generated perspective at a time`

Purpose: follow the supervisor's sequence. An individual judgment is a reference assignment, not a recall score.

```latex
Each of five LLM judges receives one generated perspective at a time, together with the topic, target population, and five reference perspectives. The judge selects the reference expressing the same underlying side and stance, or returns no match. Thematic overlap alone is insufficient. An output voiced from outside the target population also receives no match. In the saved judgments, no output was flagged as voiced from outside that population. Each judge makes five such assignments for a model's five outputs on a topic. Judges do not see one another's decisions, and recall is calculated only after their assignments have been collected.
```

### Change 05 — Preserve the concrete scoring explanation

**Replace original lines 343–370.** [Open location](/Users/vuk/Downloads/Vuk_First_Journal_Paper/0_version_2.tex:343)

Anchor: `\subsubsection{From assignments to recall}`

Purpose: this is the methodological core. Keep the example, denominators, averaging order and incomplete-panel exception. The equations and results are unchanged.

```latex
\subsubsection{From assignments to recall}
\label{sec:recall}
Recall measures the proportion of the five reference perspectives recovered by a model's five outputs. A repeated match does not recover an additional reference. We calculate recall in three steps.

\paragraph{Step 1: calculate recall for one judge.}
In the worked example (Tables~\ref{tab:reference-example} and~\ref{tab:fracking-matches}), Claude Sonnet~5 assigns GPT~5.5's five outputs to references 2, 2, 1, 5, and 1. These assignments recover three distinct references, so this judge's recall is $3/5=0.60$. All five outputs match a reference, but they cover only three. Precision counts matching outputs; recall counts distinct references recovered.

\paragraph{Step 2: combine the judges for one model and topic.}
Let $m$ identify the model, $t$ the topic, and $j$ the judge. Write $R_{mtj}$ for recall calculated from judge $j$'s assignments. When all five judges supply valid decisions for all five outputs, model-topic recall is their mean:
\begin{equation}
R_{mt}=\frac{1}{5}\sum_{j=1}^{5}R_{mtj}.
\label{eq:mean-judge-recall}
\end{equation}
In the example, the five recalls are 0.60, 0.60, 0.60, 0.60, and 0.40, giving $R_{mt}=0.56$. Judges need not agree on which references were recovered; there is no majority-vote threshold.

When judgments are missing, the available judges can differ between outputs. The calculation therefore splits duplicate matches within each judge, averages the resulting credits over valid judges for each output, and caps each reference's total credit at one. Appendix~\ref{app:recall_aggregation} gives the exact equations, which reduce to Eq.~\ref{eq:mean-judge-recall} for complete panels. Every output has at least four valid judgments. A missing judgment is excluded; a valid no-match decision remains and earns zero credit.

\paragraph{Step 3: summarise a model across topics.}
We give each topic equal weight. Overall recall averages the $16$ model-topic scores; WEIRD and Serbian recall each average eight:
\begin{equation}
\overline R_m=\frac{1}{16}\sum_{t=1}^{16}R_{mt}
=\frac{\overline R_m^{\mathrm W}+\overline R_m^{\mathrm S}}{2}.
\label{eq:model-recall}
\end{equation}
Here, $\overline R_m^{\mathrm W}$ and $\overline R_m^{\mathrm S}$ denote the model's mean recall on WEIRD and Serbian topics. To describe a topic across models, we instead average its scores over the $13$ generators. Precision and F1 are defined in Appendix~\ref{app:precision_aggregation} and reported in Appendix~\ref{app:prf-results}.
```

### Change 06 — Shorter statistical-methods subsection

**Replace original lines 372–396.** [Open location](/Users/vuk/Downloads/Vuk_First_Journal_Paper/0_version_2.tex:372)

Anchor: `\subsubsection{Comparisons and statistical analysis}`

Purpose: retain one primary test and explain the limited exploratory comparisons together. The four RQ2 and two RQ3 comparison families remain exactly as in the original. The primary comparison holds the selected models fixed and uses eight topic pairs, not 104 independent model-pair observations.

```latex
\subsubsection{Comparisons and statistical analysis}
\label{sec:statistics}

\paragraph{RQ1: compare the eight matched pairs.}
For each model $m$ and matched pair $p$, we subtract Serbian recall from WEIRD recall:
\begin{equation}
d_{mp}=R_{mp}^{\mathrm W}-R_{mp}^{\mathrm S}.
\label{eq:pair-gap}
\end{equation}
Positive differences favour the WEIRD topic. We then average the $13$ model differences within each pair:
\begin{equation}
\Delta_p=\frac{1}{13}\sum_{m=1}^{13}d_{mp}.
\label{eq:pair-mean}
\end{equation}
The primary analysis therefore uses eight pair-level differences. We report their mean and a $95\%$ $t$-based confidence interval with seven degrees of freedom. This interval assumes independent, approximately normally distributed pair-level differences. We test the hypothesised positive shift using an exact one-sided Wilcoxon signed-rank test, which assumes independent differences and symmetry under the null. The interval describes the arithmetic mean; the signed-rank test assesses a directional shift. The $104$ model-pair differences are not independent replications. Supplementary calculations appear in Appendix~\ref{app:statistics}.

\paragraph{RQ2: describe models and compare categories.}
We report overall, WEIRD, and Serbian recall for each model. For category comparisons, we first average the two topics within each matched pair and then average across models within each category, giving models equal weight. We compare the three categories pairwise and compare Frontier with all eight open-weight models combined. Individual-model intervals and pairwise tests are supplementary.

\paragraph{RQ3: compare developer groups.}
We compare eight models from US developers with four from Chinese developers, weighting models equally within each group. Mistral is excluded only from this comparison. We examine two outcomes: overall recall and the WEIRD-minus-Serbian recall gap.

For RQ2 and RQ3, each comparison uses eight pair-level contrasts and an exact two-sided sign-flip test. We apply Holm adjustment across the four RQ2 comparisons and, separately, across the two RQ3 comparisons. These exploratory tests hold the selected models fixed and assume independent contrasts whose signs are exchangeable under the null. They do not isolate effects of model category or developer country. Appendices~\ref{app:category-tests} and~\ref{app:country-tests} give the calculations and supplementary uncertainty estimates. Reported $p$-values for these group comparisons are Holm-adjusted unless stated otherwise.

\paragraph{Check judge consistency.}
We report nominal Krippendorff's $\alpha$ overall and separately for WEIRD and Serbian topics, together with judge-level no-match rates. We also recalculate scores after removing each judge in turn. These checks assess agreement and sensitivity to panel membership; they do not establish that the judgments are correct. Additional agreement measures and detailed results appear in Appendix~\ref{app:reliability}.
```

### Change 07 — Primary results

**Replace original lines 401–407.** [Open location](/Users/vuk/Downloads/Vuk_First_Journal_Paper/0_version_2.tex:401)

Anchor: `Mean recall is $0.581$ for WEIRD topics and $0.594$ for Serbian topics.`

Purpose: remove the second interval, upper bound, median and rank-biserial value from the main result. Preserve them in the statistical appendix. Keep the observed heterogeneity across topics.

```latex
Mean recall is $0.581$ for WEIRD topics and $0.594$ for Serbian topics. Across the eight matched pairs, the mean WEIRD-minus-Serbian difference is $-1.3$ percentage points ($95\%$ CI: $-10.3$ to $7.7$). The primary test finds no evidence for the hypothesised WEIRD advantage ($p=0.680$). The interval includes differences in both directions, so the result does not establish equivalent coverage.

Four matched pairs favour WEIRD topics and four favour Serbian topics. The largest differences point in opposite directions: recall is $19.1$ percentage points higher for German immigration than for its Serbian migration-route counterpart, but $16.9$ points lower for Canadian residential schools than for Srebrenica. Mean topic recall ranges from $0.449$ for the Serbian migration-route topic to $0.685$ for Serbia's West-versus-Russia alignment. Both extremes occur among the Serbian topics, indicating that topic-level variation does not follow a uniform cultural direction.

Figure~\ref{fig:paired-recall} shows all eight pair-level differences. Additional analyses and alternative uncertainty estimates are reported in Appendix~\ref{app:statistics}; they do not change the interpretation of the primary comparison. Appendix~\ref{app:paired-views} presents the model-level and individual model-pair views.
```

### Change 08 — Match the primary figure to the primary interval

**Replacement now generated:** [PNG](/Users/vuk/Downloads/BWEIRD/output/change08/primary_pair_gaps.png), [vector PDF](/Users/vuk/Downloads/BWEIRD/output/change08/primary_pair_gaps.pdf), and [two-step replacement instructions with the complete figure block](/Users/vuk/Downloads/BWEIRD/output/change08/README.md). The original manuscript and image have not been overwritten. The dependency below is satisfied once the new image is placed in the paper's `plots` folder.

**Replace original lines 412–412.** [Open location](/Users/vuk/Downloads/Vuk_First_Journal_Paper/0_version_2.tex:412)

Anchor: `\caption{Primary cultural comparison.`

**Dependency: update the actual figure before applying this caption.** The image included at original line 411 is [plots/primary_pair_gaps.png](/Users/vuk/Downloads/Vuk_First_Journal_Paper/plots/primary_pair_gaps.png). The current caption identifies its mean interval as a bootstrap interval. Changing only the caption would mislabel the analysis.

Keep the eight points, their labels and the mean diamond. Replace only the mean's interval and any legend identifying that interval. The saved primary summary gives:

| Quantity | Recall units | Percentage points |
|---|---:|---:|
| Mean gap | −0.013076923076923075 | −1.3076923076923075 |
| Lower t bound | −0.102918289999674 | −10.2918289999674 |
| Upper t bound | 0.07676444384582787 | 7.676444384582787 |

These are existing values from [weird_gap_summary.csv](/Users/vuk/Downloads/BWEIRD/results/agg/weird_gap_summary.csv), row `pooled_coverage`, columns `mean_gap`, `mean_t_lo`, and `mean_t_hi`. Use the units of the plot axis. Do not generate new estimates from rounded manuscript values. The existing plotting code is [figures/reproduce.py](/Users/vuk/Downloads/BWEIRD/figures/reproduce.py); this guide does not modify it or the image.

After regenerating the image, use:

```latex
\caption{Recall differences for the eight matched topic pairs. Each point is the WEIRD-minus-Serbian difference averaged over the $13$ generators; positive values favour WEIRD topics. The diamond shows the mean across pairs, with the $95\%$ $t$-based confidence interval used in the primary analysis. Pair-specific confidence intervals are not shown.}
```

### Change 09 — RQ2 opening

**Replace original lines 418–418.** [Open location](/Users/vuk/Downloads/Vuk_First_Journal_Paper/0_version_2.tex:418)

Anchor: `Table~\ref{tab:model-recall} reports perspective recall`

Purpose: show what the descriptive model table establishes, and direct readers to the supplementary inferential analysis without foregrounding the unstable count of significant comparisons.

```latex
Table~\ref{tab:model-recall} reports overall recall and separate means for WEIRD and Serbian topics. Overall recall ranges from $0.458$ for Llama 3.3 70B to $0.698$ for Gemini 3.1 Pro. Even the highest-recall model leaves approximately $30\%$ of the reference coverage unrecovered on average. These are descriptive comparisons of the selected models; the ordering does not establish that every difference between models is statistically distinguishable. Model-level intervals and pairwise tests appear in Appendices~\ref{app:prf-results}, \ref{app:bootstrap}, and~\ref{app:pairwise_results}.
```

### Change 10 — Simpler main model table

**Replace original lines 420–449.** [Open location](/Users/vuk/Downloads/Vuk_First_Journal_Paper/0_version_2.tex:420)

Anchor: `\caption{Perspective recall by model category.`

Purpose: remove repeated interval clutter from the descriptive table. Every mean, model and category membership is unchanged. All 13 intervals are already reproduced in the supplementary precision/F1 table at original lines 903–929; they are not lost.

```latex
\begin{table*}[!t]
\centering
\small
\caption{Perspective recall by model category. Each topic receives equal weight. Models are ordered by overall recall within each category. Supplementary intervals are reported in Appendix~\ref{app:prf-results}, with the matched-pair sensitivity analysis described in Appendix~\ref{app:bootstrap}.}
\label{tab:model-recall}
\begin{tabular}{lccc}
\toprule
Model & Overall recall & WEIRD & Serbian \\
\midrule
\multicolumn{4}{l}{\textit{Frontier/API systems (5)}}\\
Gemini 3.1 Pro & $0.698$ & $0.675$ & $0.720$\\
GPT 5.5 & $0.645$ & $0.635$ & $0.655$\\
Qwen 3.7 Max & $0.582$ & $0.545$ & $0.618$\\
Claude Opus 4.8 & $0.578$ & $0.530$ & $0.625$\\
Grok 4.3 & $0.575$ & $0.565$ & $0.585$\\
\addlinespace
\multicolumn{4}{l}{\textit{Larger open-weight systems (6)}}\\
DeepSeek V4 Pro & $0.645$ & $0.650$ & $0.640$\\
GLM 5.2 & $0.607$ & $0.660$ & $0.554$\\
Kimi K2.6 & $0.604$ & $0.595$ & $0.614$\\
Mistral Large 3 & $0.565$ & $0.545$ & $0.585$\\
GPT-OSS 120B & $0.541$ & $0.570$ & $0.513$\\
Llama 4 Maverick & $0.502$ & $0.520$ & $0.485$\\
\addlinespace
\multicolumn{4}{l}{\textit{Smaller open-weight systems (2)}}\\
Gemma 4 31B & $0.638$ & $0.598$ & $0.679$\\
Llama 3.3 70B & $0.458$ & $0.465$ & $0.450$\\
\bottomrule
\end{tabular}
\end{table*}
```

### Change 11 — Concise category comparison

**Replace original lines 451–451.** [Open location](/Users/vuk/Downloads/Vuk_First_Journal_Paper/0_version_2.tex:451)

Anchor: `The mean recall of the selected models is $0.615$`

Purpose: report the observed difference and its adjusted result. Move the raw p-value and the smallest adjusted value in the family to the appendix rather than highlighting several thresholds in the main text.

```latex
Mean recall is $0.615$ for Frontier systems, $0.578$ for larger open-weight systems, and $0.548$ for smaller open-weight systems. Across all eight open-weight models, mean recall is $0.570$. The observed Frontier advantage over this combined group is therefore $4.5$ percentage points ($p=0.258$). None of the four category comparisons reaches the $0.05$ threshold after adjustment (Appendix~\ref{app:category-tests}). These results do not establish equivalence or isolate effects of size, openness, or capability.
```

### Change 12 — Preserve the panel-composition qualification

**Replace original lines 453–453.** [Open location](/Users/vuk/Downloads/Vuk_First_Journal_Paper/0_version_2.tex:453)

Anchor: `Individual models also vary substantially within categories.`

Purpose: remove the reference to overlapping intervals from the main narrative once those intervals are supplementary. Keep the concrete evidence that judge panels can affect model comparisons.

```latex
Individual models vary substantially within categories. Gemma 4 31B has recall $0.638$, close to the $0.645$ reported for GPT 5.5 and DeepSeek V4 Pro, whereas Llama 3.3 70B has recall $0.458$. These observed similarities do not establish equivalence. Comparisons also depend on panel composition: Gemini 3.1 Pro matched $52.7\%$ of the outputs it judged, compared with $65.0$--$76.6\%$ for the other judges. Removing it raises individual model recall by up to $3.6$ percentage points (Appendix~\ref{app:lojo}). Google's two generators are never scored by this judge because of the family-disjoint design. Small differences between their scores and those of other generators therefore require caution.
```

### Change 13 — RQ3 overall recall, stated once

**Replace original lines 457–458.** [Open location](/Users/vuk/Downloads/Vuk_First_Journal_Paper/0_version_2.tex:457)

Anchor: `The four models from Chinese developers had mean overall recall`

Purpose: report the overall-recall contrast here. Report the cultural-gap contrast only after the table in Change 14. Preserve the existing pair-bootstrap interval; only its method name moves to the appendix.

```latex
The four models from Chinese developers have mean overall recall $0.609$, compared with $0.579$ for the eight models from US developers (Table~\ref{tab:origin-recall}). The US-minus-China difference is $-3.0$ percentage points ($95\%$ CI: $-4.8$ to $-1.3$; $p=0.047$). This exploratory comparison holds the selected models fixed. It provides evidence of a difference between these groups on this benchmark, but does not identify an effect of developer country.
```

Keep the developer-group table at original lines 460–474, including its label `tab:origin-recall`, unchanged.

### Change 14 — RQ3 cultural gap and interpretation

**Replace original lines 476–478.** [Open location](/Users/vuk/Downloads/Vuk_First_Journal_Paper/0_version_2.tex:476)

Anchor: `The groups' cultural gaps differ less conclusively.`

Purpose: distinguish the overall recall difference from the difference between cultural gaps. Retain the important group-composition sensitivity from the original opening paragraph.

```latex
The mean WEIRD-minus-Serbian gap is $-1.9$ percentage points in the US group and $+0.6$ points in the Chinese group. The US-minus-China difference between these gaps is $-2.5$ points ($95\%$ CI: $-8.2$ to $2.5$; $p=0.453$). We therefore do not detect a difference between the groups' cultural gaps (Appendix~\ref{app:country-tests}).

The groups differ in composition. The Chinese group contains one Frontier model and three larger open-weight models; the US group contains four Frontier, two larger open-weight, and two smaller open-weight models. Only the US group includes smaller open-weight systems. Excluding them reduces the observed overall US-minus-China difference from $-3.0$ to about $-2.0$ percentage points. Some US developers also contribute more than one model. These comparisons consequently describe the selected systems and cannot establish that Chinese models generally perform better or that developer country causes the observed difference.
```

### Change 15 — One main judge-agreement coefficient

**Replace original lines 480–500.** [Open location](/Users/vuk/Downloads/Vuk_First_Journal_Paper/0_version_2.tex:480)

Anchor: `\subsection{Descriptive checks on judge consistency}`

Purpose: retain a judge check that is easy to read. Alpha values below are the existing alpha column, not renamed kappa values. The original three-column table is preserved in Change 26 with a distinct appendix label.

```latex
\subsection{Descriptive checks on judge consistency}
\label{sec:judge-checks}
Judge agreement is similar across the two settings: Krippendorff's $\alpha$ is $0.762$ for WEIRD topics and $0.775$ for Serbian topics (Table~\ref{tab:judge-checks}). The corresponding judge-level no-match rates are $32.9\%$ and $31.1\%$ of valid decisions. Additional agreement measures appear in Appendix~\ref{app:agreement_coefficients}.

\begin{table}[!htbp]
\centering
\small
\caption{Descriptive judge agreement, measured by nominal Krippendorff's $\alpha$. Agreement measures consistency, not correctness or absence of shared bias.}
\label{tab:judge-checks}
\begin{tabular*}{\columnwidth}{@{\extracolsep{\fill}}lc@{}}
\toprule
Scope & $\alpha$\\
\midrule
All topics & $0.769$\\
WEIRD topics & $0.762$\\
Serbian topics & $0.775$\\
\bottomrule
\end{tabular*}
\end{table}

Removing one judge at a time changes the pooled WEIRD-minus-Serbian recall gap from $-1.3$ percentage points to values between approximately $-2.0$ and $-0.8$ points (Appendix~\ref{app:lojo}). The observed mean gap therefore remains small and negative under each removal. This does not establish equal judge error rates across settings: several judges may agree on the same incorrect match.
```

The shortened paragraph concentrates on the primary cultural result. Detailed ranking sensitivity remains in the appendix; do not expand a statement verified for F1 rankings into a claim about recall rankings without checking the corresponding output.

### Change 16 — Discussion of the primary comparison

**Replace original lines 509–509.** [Open location](/Users/vuk/Downloads/Vuk_First_Journal_Paper/0_version_2.tex:509)

Anchor: `Neither the pooled analysis nor the per-model comparisons`

```latex
The primary matched-pair comparison provides no evidence for the predicted WEIRD recall advantage. Judge agreement was also similar across the two settings, although this does not establish equal error rates. These findings concern the selected controversies under direct elicitation in English. They do not establish equal representation across cultures, languages, or tasks.
```

### Change 17 — Discussion of model categories

**Replace original lines 519–519.** [Open location](/Users/vuk/Downloads/Vuk_First_Journal_Paper/0_version_2.tex:519)

Anchor: `Model performance also overlaps across access and size categories`

Purpose: preserve the descriptive overlap and adjusted findings without suggesting that the analysis proves the categories have no predictive value.

```latex
Recall varies within each access and size category, and individual scores overlap across categories. Although the observed category means differ, none of the four exploratory comparisons reaches the adjusted significance threshold. These results do not establish equivalence between categories or identify the effects of size and openness separately.
```

### Change 18 — Judge-validity limitation

**Replace original lines 541–541.** [Open location](/Users/vuk/Downloads/Vuk_First_Journal_Paper/0_version_2.tex:541)

Anchor: `The scores depend on LLM judgments of whether generated and reference perspectives`

```latex
The scores depend on LLM judgments of whether generated and reference perspectives express the same stance. Agreement and judge-removal checks describe consistency and sensitivity to panel membership. They do not establish correctness, because judges may share errors. Excluding judges from the generator's developer family prevents direct within-family evaluation but does not remove shared biases or differences in judge strictness.
```

### Change 19 — Shorter statistical-resolution limitation

**Replace original lines 545–545.** [Open location](/Users/vuk/Downloads/Vuk_First_Journal_Paper/0_version_2.tex:545)

Anchor: `The primary comparison rests on eight topic pairs`

Purpose: explain what the small number of pairs means for interpretation without introducing a second testing framework and a power calculation into the main discussion.

```latex
The primary comparison rests on eight topic pairs whose recall differences vary widely (SD $10.7$ percentage points). The $95\%$ confidence interval for the mean gap spans $-10.3$ to $7.7$ points, leaving differences in either direction compatible with the data under the interval's assumptions. Eight investigator-selected pairs provide limited statistical resolution and do not represent a random sample of cultural controversies. We therefore report no detectable WEIRD advantage, not equivalent coverage. Alternative intervals and an illustrative sensitivity calculation appear in Appendix~\ref{app:bootstrap}.
```

## 4. Appendix replacements and preservation of removed detail

### Change 20 — Separate the primary interval from supplementary calculations

**Replace original lines 783–787.** [Open location](/Users/vuk/Downloads/Vuk_First_Journal_Paper/0_version_2.tex:783)

Anchor: `\subsection{Bootstrap confidence intervals}`

Purpose: the existing subsection now contains several procedures. Name their roles explicitly. Retain the old label `app:bootstrap` so existing references continue to work.

```latex
\subsection{Confidence intervals and sensitivity calculations}
\label{app:bootstrap}

\paragraph{Primary interval for the mean cultural gap.}
Let $\overline\Delta$ and $s_\Delta$ be the mean and sample standard deviation of the eight pair-level differences. The primary $95\%$ confidence interval is
\[
\overline\Delta\ \pm\ t_{0.975,7}\frac{s_\Delta}{\sqrt{8}}.
\]
The mean is $-0.0131$, the SD is $0.107$, and the SE is $0.038$. The resulting interval is $[-0.103,0.077]$, or $-10.3$ to $7.7$ percentage points. The calculation assumes independent, approximately normally distributed pair-level differences. It estimates the arithmetic mean and is separate from the signed-rank test in Appendix~\ref{app:primary_wilcoxon}.

\paragraph{Supplementary interval and upper bound.}
The original percentile bootstrap resamples the eight matched pairs $10{,}000$ times, keeping all $13$ models together within each sampled pair. It uses seed $42$ and the saved random-number stream, giving $[-0.08096,0.05823]$. With only eight resampling units, percentile intervals may have limited coverage accuracy. The corresponding one-sided $95\%$ $t$ upper bound is $0.059$. This is conditional on the interval assumptions and the selected benchmark, not a general upper bound on cultural disparities.

\paragraph{Individual-model intervals.}
Table~\ref{tab:prf-supplement} retains the original $95\%$ percentile intervals for model-level recall, precision, and F1, based on $10{,}000$ resamples of the $16$ individual topics. These intervals do not retain matched-pair blocks. A sensitivity analysis for model recall instead resamples the eight matched pairs, retaining both topics and their equal weights, with $10{,}000$ resamples and a fresh NumPy generator using seed $42$. Both sets of recall intervals are supplied in the accompanying analysis files. The model means are unchanged. Neither overlapping intervals nor an absence of significant pairwise differences establishes model equivalence.

\paragraph{Illustrative sensitivity calculation.}
For a one-sided one-sample $t$-test at $\alpha=0.05$, normally distributed independent pair-level differences, and the observed between-pair SD, a hypothetical five-percentage-point WEIRD advantage gives approximately $32\%$ power. An advantage of about $10.5$ points gives $80\%$ power. These values use a noncentral $t$ distribution with seven degrees of freedom. They describe hypothetical effects under a $t$-test, not power at the observed effect or power of the exact Wilcoxon test.
```

### Change 21 — Signed-rank results in the appendix

**Replace original lines 813–813.** [Open location](/Users/vuk/Downloads/Vuk_First_Journal_Paper/0_version_2.tex:813)

Anchor: `All eight differences are non-zero, and no two have the same absolute value`

Keep the eight observed differences at lines 804–812 unchanged. The following text preserves every result from the original paragraph.

```latex
All eight differences are non-zero, and no two have the same absolute value, so there are no tied ranks. The primary exact Wilcoxon signed-rank test uses a one-sided alternative of a positive shift in WEIRD-minus-Serbian recall and gives $p=0.6797$. The observed mean difference is $-0.0131$, and the median is $-0.0140$. For completeness, the two-sided result is $p=0.7422$, and the matched-pairs rank-biserial correlation is $-0.1667$. The signed-rank inference assumes independent pair-level differences and symmetry under the null; it does not directly test the arithmetic mean.
```

### Change 22 — Category-test appendix

**Replace original lines 832–834.** [Open location](/Users/vuk/Downloads/Vuk_First_Journal_Paper/0_version_2.tex:832)

Anchor: `For each model and matched pair, we first average WEIRD and Serbian recall.`

Purpose: retain the full comparison family and the numerical detail removed from the main category paragraph. The exact sign-flip procedure requires sign-exchangeability; this is not guaranteed merely by having paired data. [Permutation-inference reference](https://pmc.ncbi.nlm.nih.gov/articles/PMC4010955/)

```latex
For each model and matched pair, we first average WEIRD and Serbian recall. We then average across models within each category, weighting models equally. Each category contrast therefore contains eight pair-level differences. The test statistic is their mean. Exact two-sided sign-flip tests enumerate all $2^8=256$ sign assignments and compare the absolute permuted mean with the absolute observed mean. These tests assume independent, sign-exchangeable pair-level contrasts and hold the selected models fixed.

Holm correction is applied jointly to four overall-recall contrasts: the three pairwise comparisons among Frontier/API, larger open-weight, and smaller open-weight systems, and Frontier/API versus all eight open-weight models combined. The Frontier-versus-combined-open-weight difference is $0.045$, with raw $p=0.086$ and adjusted $p=0.258$. None of the four comparisons meets the adjusted $0.05$ threshold. The smallest adjusted value is $0.063$, for Frontier versus smaller open-weight systems. The accompanying analysis files contain all four contrasts, including raw and adjusted $p$-values.
```

### Change 23 — Developer-group appendix

**Replace original lines 840–840.** [Open location](/Users/vuk/Downloads/Vuk_First_Journal_Paper/0_version_2.tex:840)

Anchor: `We compare overall recall and, separately, the WEIRD-Serbian recall gap.`

Keep the group-membership paragraph at line 838 unchanged. This replacement preserves both tests, both intervals and both raw and adjusted results.

```latex
We compare overall recall and, separately, the WEIRD-minus-Serbian recall gap. Models receive equal weight within each group. For each outcome, we calculate a US-minus-China contrast within each matched pair, giving eight contrasts. Exact two-sided sign-flip tests enumerate all $2^8=256$ sign assignments, using the mean contrast as the statistic. The tests assume independent, sign-exchangeable pair-level contrasts and hold the selected models fixed. Confidence intervals are percentile intervals from $10{,}000$ resamples of the eight matched pairs. Holm correction is applied across the two tests.

For overall recall, the US-minus-China difference is $-0.030$ ($95\%$ CI $[-0.048,-0.013]$), with raw $p=0.023$ and Holm-adjusted $p=0.047$. For the cultural gap, the difference is $-0.025$ ($95\%$ CI $[-0.082,0.025]$), with raw and adjusted $p=0.453$. These outcomes answer different questions: an overall recall difference does not establish a difference in the WEIRD-Serbian gap. The accompanying analysis files contain both contrasts and their uncertainty estimates.
```

### Change 24 — Role of supplementary model intervals and metrics

**Replace original lines 905–905.** [Open location](/Users/vuk/Downloads/Vuk_First_Journal_Paper/0_version_2.tex:905)

Anchor: `Table~\ref{tab:prf-supplement} reports the saved model-level recall`

Purpose: the existing supplementary table already contains all intervals removed from the main model table. Retain the table and its numbers at lines 906–929 unchanged.

```latex
Table~\ref{tab:prf-supplement} preserves the model-level recall intervals and supplementary precision and F1 summaries from the saved analysis. Recall remains the primary outcome. F1 is the harmonic mean of model-level precision and recall, not an average of topic-level F1 scores. The displayed intervals use the original $10{,}000$-resample individual-topic bootstrap. Appendix~\ref{app:bootstrap} explains its distinction from the matched-pair recall sensitivity analysis supplied with the accompanying files. An unmatched output may express a legitimate position outside the reference set.
```

### Change 25 — Preserve the pairwise-testing sensitivity result

**Replace original lines 934–934.** [Open location](/Users/vuk/Downloads/Vuk_First_Journal_Paper/0_version_2.tex:934)

Anchor: `The full $78$-row table is supplied in GitHub repository.`

Purpose: removing the main-text claim about 15 comparisons must not conceal the pair-blocked result that qualifies it. Keep both results together. Leave the technical procedure at lines 842–870 and the per-model tests at lines 872–883 and 936–973 intact.

```latex
The $78$ pairwise model comparisons are supplementary and are not used to establish an inferential ranking in the main paper. The accompanying analysis files report mean recall differences, raw $p$-values, and Benjamini--Hochberg-adjusted $p$-values for the procedures in Appendix~\ref{app:model_pair_tests}. Fifteen comparisons survive adjustment when the $16$ topics are treated as separate sign-flip units, both with the original Monte Carlo calculation and with exhaustive enumeration. None survives when the eight matched pairs are retained as blocks; the smallest adjusted $p$-value is $0.087$. The mean differences are unchanged. This sensitivity concerns the inferential unit, not merely Monte Carlo sampling. Neither result establishes equivalence between models.
```

### Change 26 — Preserve the full agreement table in the appendix

**Replace original lines 978–985.** [Open location](/Users/vuk/Downloads/Vuk_First_Journal_Paper/0_version_2.tex:978)

Anchor: `\subsection{Agreement coefficients}`

Purpose: use alpha in the main paper while keeping the other computed coefficients available. This introduces one new table label, `tab:agreement-supplement`; do not reuse the main table's `tab:judge-checks` label here.

```latex
\subsection{Agreement coefficients}
\label{app:agreement_coefficients}
The main paper reports nominal Krippendorff's $\alpha$, which accommodates multiple judges and missing ratings. Table~\ref{tab:agreement-supplement} also preserves Fleiss' $\kappa$ and Gwet's AC1 from the original analysis. The pipeline excludes missing ratings and uses variable-rater formulations for $\kappa$ and AC1. These coefficients use different chance-agreement calculations; they need not agree in general. Their similar values here support the same descriptive account of judge consistency, but do not establish accuracy or equal error rates across cultural settings.

\begin{table}[!htbp]
\centering
\small
\caption{Supplementary agreement coefficients. The main paper reports the $\alpha$ column; all three measures describe consistency rather than correctness.}
\label{tab:agreement-supplement}
\begin{tabular*}{\columnwidth}{@{\extracolsep{\fill}}lccc@{}}
\toprule
Scope & $\kappa$ & AC1 & $\alpha$\\
\midrule
All topics & $0.768$ & $0.783$ & $0.769$\\
WEIRD topics & $0.761$ & $0.777$ & $0.762$\\
Serbian topics & $0.774$ & $0.789$ & $0.775$\\
\bottomrule
\end{tabular*}
\end{table}
```

### Supplementary sections to retain

| Original lines | Section / content | Reason to retain |
|---|---|---|
| 579–687 | Generation and judging prompts | Reproduction of what was actually requested from each model |
| 692–715 | Judge panels | Family exclusions and substitutions |
| 717–720 | Reference-order randomisation | Mapping displayed indices back to canonical identifiers |
| 722–778 | Aggregation and missing judgments | Actual scoring algorithm, including duplicate credits, cap and execution counts |
| 789–812 | Primary signed-rank setup and eight observed values | Transparent definition of the primary analysis |
| 815–828 | Alternative aggregation, crossed resampling and model-pair mixed model | Preserve completed robustness checks, assumptions and boundary warning |
| 842–883 | Pairwise and per-model test algorithms | Preserve corrections, ties/zeros handling and numerical settings |
| 885–888 | Per-reference mixed-effects check | Keep distinct from the model-pair mixed model and retain its dependence caveat |
| 893–901 | Paired views at three descriptive levels | Shows heterogeneity without treating 104 cells as independent replicates |
| 906–929 | Supplementary recall, precision and F1 table | Retains the intervals removed from the main table |
| 936–973 | Per-model cultural comparisons | Retains all 13 tests and their BH-adjusted values |
| 987–1004 | Pairwise judge agreement, judge removal and no-match denominators | Preserves the audit trail and the difference between missing and valid no-match decisions |
| 1010–1066 | Worked fracking example | Makes scoring inspectable and reproducible |
| 1068–1100 | Execution records and model identifiers | Identifies the evaluated model snapshot and settings |

## 5. Conditional alternative: if the one-sided choice was not made in advance

The default draft preserves the currently designated primary test. If the historical record does not support that designation, use the already reported two-sided result as primary and document the reporting change. The effect estimate and interval do not change. Do not claim that this choice was preregistered.

Make these coordinated substitutions in the proposed replacements:

| Location | Substitution |
|---|---|
| Change 01, abstract | Replace `with no evidence for the hypothesised WEIRD advantage ($p=0.680$)` with `with no detectable difference between settings ($p=0.742$)` |
| Change 06, methods | Replace the two sentences beginning `We test the hypothesised positive shift` and `The interval describes` with the methods wording below |
| Change 07, RQ1 result | Replace `The primary test finds no evidence for the hypothesised WEIRD advantage ($p=0.680$).` with `The primary test does not detect a difference between settings ($p=0.742$).` |
| Change 21, appendix | Replace the paragraph with the appendix wording below |

Methods wording:

```latex
We use an exact two-sided Wilcoxon signed-rank test to assess a shift in either direction, assuming independent differences and symmetry under the null. The interval describes the arithmetic mean; the signed-rank test assesses a distributional shift. The directional result corresponding to the hypothesised WEIRD advantage is reported separately in Appendix~\ref{app:primary_wilcoxon}.
```

Appendix wording:

```latex
All eight differences are non-zero, and no two have the same absolute value, so there are no tied ranks. The exact two-sided Wilcoxon signed-rank test gives $p=0.7422$. The observed mean difference is $-0.0131$, and the median is $-0.0140$. For the directional alternative of a positive shift in WEIRD-minus-Serbian recall, the one-sided result is $p=0.6797$. The matched-pairs rank-biserial correlation is $-0.1667$. The signed-rank inference assumes independent pair-level differences and symmetry under the null; it does not directly test the arithmetic mean.
```

The supplementary per-model tests can remain labelled as the directional exploratory analyses that were performed. Do not silently relabel their p-values as two-sided.

## 6. Application and verification

### What is ready to copy

Changes 01–26 contain the proposed LaTeX replacements. All locations refer to the original source snapshot. Existing labels are retained, and the agreement appendix gains only `tab:agreement-supplement`. The model table preserves the 13 models, the 5/6/2 category split, and all recall means. The agreement tables use the existing values for each coefficient.

**Guide verification completed:** all 26 replacement ranges and searchable anchors were checked against the source. An in-memory application confirmed non-overlapping edits, preservation of existing labels, no new unresolved cross-references, balanced LaTeX environments, and unchanged model-table means. Alpha values were checked against the saved agreement output. All local links resolve, and the source checksum is unchanged. This is a source-level check, not confirmation of successful LaTeX compilation or final PDF layout.

### What requires an accompanying action

- **Figure:** Change 08 requires regenerating the plotted interval, not just editing the caption. Use the saved t limits specified there. This guide has not changed that asset.
- **Primary-test history:** Check the timing of the directional testing decision before choosing between the default draft and Section 5. The guide does not resolve that historical fact.
- **Supplementary files:** Keep the full 78-comparison table, all 13 per-model tests, both model-interval versions, category/developer contrasts and their calculation code available with the paper. A generic repository reference is not a substitute for delivering those files. The manuscript's existing repository-placeholder issue at line 569 remains to be resolved before submission.
- **Compilation after application:** Build the integrated manuscript, resolve references and inspect table/figure layout. This Markdown guide is not a compiled revised paper, and its snippets have not been typeset together with the full manuscript.

### Final editorial checks after applying the guide

1. The abstract, RQ1 text and main figure show the same primary interval: −10.3 to 7.7 percentage points.
2. The primary test is consistently one-sided with p = .680, or consistently two-sided with p = .742 if Section 5 is used. Both exact values remain identifiable in the appendix.
3. RQ2/RQ3 main-text group-comparison p-values are explicitly defined as Holm-adjusted. The four-test RQ2 and two-test RQ3 families are unchanged.
4. Benjamini-Hochberg, Gwet's AC1, Fleiss' kappa, rank-biserial correlation, the RQ1 bootstrap alternative, the one-sided upper bound and the t-test power illustration are confined to the supplementary account, except where a brief cross-reference is needed.
5. The main judge table reports alpha values 0.769, 0.762 and 0.775. The appendix retains the original three coefficient columns with the correct labels.
6. Neither model rankings nor overlapping intervals are described as proof of significant differences or equivalence.
7. The five judgments used to evaluate one generated perspective are not confused with the five generated perspectives scored for a topic. The primary inferential unit remains the matched topic pair.
8. Missing calls remain distinct from valid no-match judgments. The incomplete-panel scoring rule is retained.
9. The worked example, prompt text, reference sets, model identifiers and generation settings remain available for replication.
10. Review all cross-references and the final rendered PDF after the actual edits; source line numbers and PDF page numbers will change.

The recommended revision leaves a main paper organised around one performance measure, a transparent scoring sequence, three clearly bounded comparisons and one main judge-agreement measure. The supplementary material retains the completed checks and the qualifications needed to interpret them.
