# Accompanying analysis supplement

This document preserves analyses moved out of the shortened article for focus and length. These are completed analyses from the supplied manuscript and saved files, not new experiments. The article retains all three research questions, their principal results, and their qualifications. Its individual-model ordering is descriptive.

The complete original source is preserved in [original_0_version_2.tex](analysis_archive/original_0_version_2.tex). The file [changed_original_passages.tex.txt](analysis_archive/changed_original_passages.tex.txt) preserves original source passages with their original line ranges. Those archived source references use the original document’s numbering; they are not revised-paper cross-references.

## A. Additional intervals and illustrative power

Original Appendix D.1, source lines 825–833:

- The original percentile bootstrap resamples eight matched pairs 10,000 times, retaining all 13 models within each pair. Its saved seed-42 stream gives a mean-gap interval of [−0.08096, 0.05823]. With only eight units, this interval may have limited coverage accuracy. It is not the primary t-based interval retained in the shortened article.
- The one-sided 95% t upper bound is 0.059, conditional on the selected benchmark and interval assumptions.
- Original individual-model intervals resample 16 separate topics. A second set resamples eight matched pairs, retaining both topics. Both use 10,000 resamples; the paired version uses a fresh NumPy generator seeded with 42. These intervals do not establish model equivalence.
- Under a hypothetical one-sided one-sample t-test with independent normally distributed pair-level differences, the observed between-pair SD, and significance level 0.05, a five-percentage-point advantage has approximately 32% power; about 10.5 points gives 80% power. These are hypothetical t-test calculations, not the power of the exact Wilcoxon test.

Files: [weird_gap_summary.csv](supplementary/weird_gap_summary.csv), [precision_recall_f1.csv](supplementary/precision_recall_f1.csv), [model_pair_bootstrap_ci.csv](supplementary/model_pair_bootstrap_ci.csv). In [sensitivity_results.json](supplementary/sensitivity_results.json), the historical `primary.mean_ci_lo/hi` fields refer to the bootstrap interval, not the t-based interval reported as primary in the current paper.

## B. Alternative aggregation and crossed checks

Original Appendix D.3, lines 860–874:

- Averaging within each of the 13 generators gives a one-sided signed-rank p = 0.843 and two-sided p = 0.331. The same eight pairs are used throughout; the selected model families are not independent cultural replications.
- A crossed bootstrap independently resamples generator rows and matched-pair columns, keeping each Cartesian-product submatrix. Across 10,000 resamples, its approximate 95% mean-gap interval is [−0.090, 0.070]. The manuscript attributes this resampling approach to Owen (2007), retained in the original bibliography.
- A crossed random-intercept model of the 104 model-pair differences estimates −0.013 (SE 0.038; 95% Wald interval [−0.088, 0.062]; approximate two-sided p = 0.733). The fit converged with a boundary warning. It is a sensitivity check, not the primary analysis.
- These checks do not establish representative sampling or explicitly model dependence among different generators from the same developer family.

Files: [paired_differences_13x8.csv](supplementary/paired_differences_13x8.csv), [sensitivity_results.json](supplementary/sensitivity_results.json).

## C. Individual-model comparisons and the matched-pair qualification

Original D.6 and E.3, lines 889–917 and 979–982:

The original comparison of each of the 78 model pairs used the mean recall difference across 16 topics and 10,000 randomly sampled sign assignments (seed 42). Its two-sided Monte Carlo p-value is (1 + the number of absolute permuted means at least as large as the observed absolute mean) / 10,001. BH adjustment covers all 78 comparisons.

A sensitivity analysis first averages the two topics in each matched pair and then enumerates all 256 sign assignments of the eight pair-level contrasts. The mean differences are unchanged. This calculation also applies BH to all 78 comparisons and uses a numerical tolerance of 10^−12 in tail comparisons.

**Fifteen comparisons survive BH adjustment when the 16 topics are treated separately, but none survives when the eight matched pairs are retained as blocks (minimum adjusted p = 0.087).** Exhaustive enumeration of all 65,536 individual-topic sign patterns still yields 15 adjusted significant comparisons. The discrepancy is therefore about the inferential unit rather than Monte Carlo error alone. Neither analysis establishes equivalence between models. This qualification remains visible in the shortened article’s RQ2 results.

Files: [pairwise_models.csv](supplementary/pairwise_models.csv), [pair_blocked_model_comparisons.csv](supplementary/pair_blocked_model_comparisons.csv).

## D. Per-model cultural tests

Original D.7 and E.4/Table 9, lines 919–930 and 984–1022:

Each generator’s test uses its eight matched WEIRD-minus-Serbian differences. Differences are rounded to 12 decimal places to remove floating-point noise; zeros are dropped; tied absolute differences receive midranks. All sign assignments for the remaining non-zero differences are enumerated. The one-sided test uses the positive-rank sum; rank-biserial correlations use the same ranks. BH adjustment covers the 13 tests. No generator has a raw one-sided p below 0.05, and none survives adjustment.

File: [weird_gap_per_model.csv](supplementary/weird_gap_per_model.csv). The original table and methods are retained in the source archive.

## E. Per-reference mixed-effects check

Original D.8, lines 932–935:

The separate model of 1,040 per-reference recall credits includes a cultural-arm fixed effect and random intercepts for matched pair and generator. It estimates the WEIRD coefficient as −0.0131 (SE 0.0268, p = 0.626). This is distinct from the 104-difference model above and does not explicitly account for all dependence among references within a model-topic response.

File: [mixed_model.csv](supplementary/mixed_model.csv).

## F. Supplementary metrics and descriptive figure

Original C.4, E.1, and E.2/Table 8:

For each generated perspective, precision credit is the fraction of valid judges matching it to any reference; model-topic precision averages the five output credits. A valid no-match decision gives zero, while a missing judgment is excluded. Model-level precision and recall average the 16 topics, and F1 is the harmonic mean of those model-level averages, not an average of topic-level F1. An unmatched output can still express a legitimate position outside the benchmark.

The archived figure shows recall at the topic-pair, model, and individual-cell levels. Its 104 cells share models and pairs and are descriptive observations, not independent replicates.

Files: [precision_recall_f1.csv](supplementary/precision_recall_f1.csv), [model_recall.csv](supplementary/model_recall.csv), [original paired-recall figure](plots/paired_recall.png). The full original table, definitions, and caption remain in the source archive.

## G. Additional agreement and judge-removal results

Original F.1–F.3, lines 1026–1057:

| Scope | Fleiss’ kappa | Gwet’s AC1 | Krippendorff’s alpha |
|---|---:|---:|---:|
| All topics | 0.768 | 0.783 | 0.769 |
| WEIRD | 0.761 | 0.777 | 0.762 |
| Serbian | 0.774 | 0.789 | 0.775 |

These coefficients have different chance-agreement calculations. Their similar values here describe consistency, not accuracy or equal cultural error rates. The shortened article uses Fleiss’ kappa alone and explicitly describes how the calculation accommodates variable numbers of valid raters.

Pairwise Cohen’s kappa ranges approximately from 0.67 to 0.85 over around 720–880 jointly rated perspectives per base-panel judge pair. The three lowest reported values are 0.671 for Gemini–Claude, 0.684 for Gemini–GPT, and 0.695 for Gemini–DeepSeek. These do not identify which judge is more accurate.

Removing each of the seven judges in turn gives Spearman correlations of 0.971–0.999 for recall rankings and 0.978–1.000 for F1 rankings relative to the full panel. Gemini 3.1 Pro remains first by F1. The pooled gap ranges from approximately −0.020 to −0.008 (full-panel gap −0.013), with reported two-sided p-values approximately 0.38–0.84. The largest recall change is +3.6 percentage points for Llama 3.3 70B after Gemini’s removal. The gap and largest-change results remain in the shortened paper.

Files: [inter_judge_agreement.csv](supplementary/inter_judge_agreement.csv), [pairwise_judge_kappa.csv](supplementary/pairwise_judge_kappa.csv), [pairwise_judge_overlap.csv](supplementary/pairwise_judge_overlap.csv), [judge_match_rates.csv](supplementary/judge_match_rates.csv).

## H. Retained group analyses and provenance

The article still reports the four Holm-adjusted model-category contrasts and the two Holm-adjusted developer-group contrasts. Their saved files are [access_group_contrasts.csv](supplementary/access_group_contrasts.csv) and [developer_country_contrasts.csv](supplementary/developer_country_contrasts.csv). In the former, the historical label “Open-weight” refers to the larger open-weight group; the combined eight-model comparison is separately labelled in that file.

The configurations, reference workbook, source ledger, and worked example are also included as copied existing records. This editing package does not claim to be a newly validated end-to-end reproducibility release: the original pipeline and complete raw outputs remain in the research workspace. The public repository identifier remains a placeholder in the manuscript and must be completed for publication.
