# Shortened paper: change guide

This is a separate revision of the supplied `0_version_2.tex`; the original source and supplied PDF have not been edited. All original-line references below refer to `/Users/vuk/Downloads/0_version_2.tex`, not to the revised file. PDF locations refer to the original 22-page PDF. They identify the relevant passage; use LaTeX line links for exact edits.

## Delivered version

- `shortened_manuscript.tex`: complete revised source, ready to use with the included dependencies.
- `shortened_manuscript.pdf`: compiled, visually checked revision.
- `ANALYSIS_SUPPLEMENT.md`: readable account of analyses moved out of the article, with links to the retained data.
- `analysis_archive/`: unchanged original source, original passages, exact diff, and validation record.
- `supplementary/`: copied analysis outputs, configurations, and source records; these are not presented as a newly audited complete public release.

The supplied PDF and a fresh compilation of the original source each have 22 pages. The revised PDF has 15 pages, using the same document style and font sizes. The conclusion moves from page 11 to page 8; references begin on page 9 instead of page 12, and the appendices begin on page 10 instead of page 13. This is a somewhat larger main-text reduction than the initial 1–2-page target, achieved by the requested consolidation rather than by shrinking the type.

## Statistical decisions

Keep one-sided Wilcoxon for RQ1, exact two-sided sign-flip tests for category and developer comparisons, Holm adjustment across the existing four and two comparison families, and Fleiss’ kappa as the sole agreement coefficient in the article. Keep the primary 95% t-based interval and a concise leave-one-judge-out check. RQ1, RQ2, and RQ3 remain word-for-word unchanged.

The kappa values are **0.768 overall, 0.761 WEIRD, 0.774 Serbian**. These replace alpha’s values; merely changing the coefficient’s name would be wrong. The values match `supplementary/inter_judge_agreement.csv`. The calculation in the existing implementation uses each item’s actual number of valid raters, averages within-item pairwise agreement, and uses pooled valid-rating frequencies for expected agreement. The revised Appendix E.1 describes that calculation. No judging was rerun.

BH is removed from the article together with the detailed individual-model inferential analyses, not stripped from retained significance claims. Those completed analyses, their adjusted p-values, and their qualifications remain in the accompanying archive. The main RQ2 result retains the finding that model-level significance depends on whether matched pairs are preserved.

## Where and what to change

| Change | Original .tex lines | Original PDF pages | Revised .tex start | Action |
|---|---|---|---|---|
| Related work | [202–227](/Users/vuk/Downloads/0_version_2.tex:202) | 2–3 | [202](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:202) | Compress the wider literature overview into two subsections; retain all its citation keys and the distinction from OvertonBench. |
| Reference construction and fracking table | [262–288](/Users/vuk/Downloads/0_version_2.tex:262) | 3–4 | [250](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:250) | Condense provenance prose; move the unchanged reference-summary table into the full worked example, now Appendix F. |
| Model list and generation procedure | [293–330](/Users/vuk/Downloads/0_version_2.tex:293) | 4–5 | [260](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:260) | Delete original Table 3; refer to the model-results table, now Table 2. Preserve developer mappings in the endpoint table, now Table 8 in Appendix G. |
| Judge procedure | [331–342](/Users/vuk/Downloads/0_version_2.tex:331) | 5–6 | [268](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:268) | Keep matching criteria, independent judging, family exclusions, reference randomisation, valid-decision counts, and missing versus no-match handling. Move the family definitions to Appendix C.1. |
| Recall explanation | [343–405](/Users/vuk/Downloads/0_version_2.tex:343) | 6 | [276](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:276) | Keep three steps, the mean-judge equation, and the real 0.56 example. Remove the equivalent reference-credit walkthrough and redundant row/column equations from the main text; the exact scoring equations remain in Appendix C.3. |
| Statistical method and agreement measure | [406–431](/Users/vuk/Downloads/0_version_2.tex:406) | 6–7 | [294](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:294) | Keep the primary Wilcoxon test, mean-gap interval, group sign-flip tests, and Holm families. Replace alpha with variable-rater Fleiss’ kappa. Do not retain unadjusted individual-model significance claims. |
| RQ1 supplementary pointers | [439–439](/Users/vuk/Downloads/0_version_2.tex:439) | 7 | [328](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:328) | Point to the retained primary appendix and accompanying analysis files instead of deleted appendix sections. |
| Individual-model findings and table caption | [451–456](/Users/vuk/Downloads/0_version_2.tex:451) | 7–9 | [337](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:337) | Keep all model means; retain the warning that individual-model significance changes when matched pairs are preserved. Describe the ordering as descriptive. |
| Judge-consistency results | [512–533](/Users/vuk/Downloads/0_version_2.tex:512) | 9 | [400](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:400) | Delete the alpha table. Report kappa 0.768 overall, 0.761 WEIRD, and 0.774 Serbian; retain no-match rates and the −2.0 to −0.8 percentage-point judge-removal range. |
| Discussion | [534–562](/Users/vuk/Downloads/0_version_2.tex:534) | 9–10 | [404](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:404) | Remove repeated result summaries. Retain the alternative explanations as untested, the implications for coverage evaluation, and the deliberation argument. |
| Limitations | [563–594](/Users/vuk/Downloads/0_version_2.tex:563) | 10–11 | [420](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:420) | Merge six subsections into four paragraphs covering reference construction, judge validity, resolution/topic selection, and population/prompting/time. |
| Missing judgments and scoring details | [779–811](/Users/vuk/Downloads/0_version_2.tex:779) | 15 | [619](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:619) | Move precision/F1 definitions to the analysis archive; merge the missing-judgment, cap, and retry explanations. Preserve the two capped credits and all execution counts. |
| Additional intervals and power | [825–833](/Users/vuk/Downloads/0_version_2.tex:825) | 16 | [629](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:629) | Keep the primary t-based interval in Appendix D.1; move alternative intervals, individual-model intervals, and illustrative t-test power to the analysis supplement. |
| Alternative aggregation and crossed checks | [860–874](/Users/vuk/Downloads/0_version_2.tex:860) | 16–17 | [669](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:669) | Remove old D.3 from the article and preserve it in the supplement. Old D.4 and D.5 become D.3 and D.4; their calculations are unchanged. |
| Individual-model tests, mixed model, secondary figures/tables | [889–1022](/Users/vuk/Downloads/0_version_2.tex:889) | 17–20 | [685](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:685) | Remove old D.6–D.8 and E.1–E.4 from the article. Preserve the full original passages and saved results separately, including the BH adjustments and the matched-pair sensitivity finding. |
| Extra agreement coefficients | [1026–1049](/Users/vuk/Downloads/0_version_2.tex:1026) | 19–20 | [688](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:688) | Replace old F.1–F.2 with one short description of the actual variable-rater kappa calculation. Alpha, AC1, and pairwise Cohen’s kappa remain in the archive only. |
| Judge-removal check | [1051–1057](/Users/vuk/Downloads/0_version_2.tex:1051) | 20 | [692](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:692) | Keep the recall-gap range and largest model-level change; move ranking correlations, F1 results, and secondary p-values to the archive. |
| Full worked example | [1069–1126](/Users/vuk/Downloads/0_version_2.tex:1069) | 20–21 | [707](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:707) | Keep the actual generated texts and all 25 assignments. Insert the reference table moved from the main text; the calculation remains 0.56. |
| Model identifiers and developer mapping | [1127–1160](/Users/vuk/Downloads/0_version_2.tex:1127) | 21–22 | [782](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:782) | Add a developer column to the existing endpoint table instead of retaining a separate main-text model table. Preserve execution dates and release-source links. |

## Exact replacements for the agreement sections

Replace original line 431 with the following methods paragraph:

```latex
We report Fleiss' $\kappa$ overall and separately for WEIRD and Serbian topics, using a variable-rater formulation that excludes missing judgments (Appendix~\ref{app:agreement_coefficients}). We also report judge-level no-match rates and recalculate recall after removing each judge in turn. These checks assess consistency and sensitivity to panel membership, not correctness.
```

Replace original lines 512–533, including the alpha table, with:

```latex
\subsection{Descriptive checks on judge consistency}
\label{sec:judge-checks}
Fleiss' $\kappa$ is $0.768$ overall, $0.761$ for WEIRD topics, and $0.774$ for Serbian topics. Judge-level no-match rates are $32.9\%$ and $31.1\%$ in the two settings. Removing one judge at a time changes the pooled WEIRD-minus-Serbian recall gap from $-1.3$ percentage points to between approximately $-2.0$ and $-0.8$ points (Appendix~\ref{app:lojo}). The observed gap remains small and negative under each removal; neither similar agreement nor this stability establishes equal judge error rates.
```

Replace original lines 1026–1049 with the following appendix subsection:

```latex
\subsection{Fleiss' kappa with incomplete panels}
\label{app:agreement_coefficients}
Each generated perspective is an item, with ratings mapped to its topic's canonical reference indices 1--5 or 0 for no match. We use the available four or five judgments per item. The variable-rater calculation averages within-item pairwise agreement, using the actual number of valid raters for each item, and estimates chance agreement from the pooled category frequencies across valid ratings. Fleiss' $\kappa$ is observed agreement minus expected agreement, divided by one minus expected agreement. Missing ratings are excluded rather than coded as no match. We calculate the coefficient overall and separately by cultural setting; it describes consistency, not accuracy.
```

## What was preserved

- The abstract, all three research questions, main model recall values, developer-group table, topic-pair table, exact generator/judge prompts, and exact aggregation equations.
- RQ1: WEIRD recall 0.581; Serbian recall 0.594; gap −1.3 percentage points; 95% interval −10.3 to +7.7 points; one-sided p = 0.680.
- RQ2: Frontier versus combined open-weight gap +4.5 points; Holm-adjusted p = 0.258; no significant category comparison after adjustment.
- RQ3: overall US-minus-China difference −3.0 points, adjusted p = 0.047; cultural-gap difference −2.5 points, adjusted p = 0.453; original confidence intervals and composition qualifications.
- The existing illustration of the primary t-based interval. Its image was checked against the embedded image in the supplied PDF; the older bootstrap illustration found in a previous project folder was not retained.
- Missing versus no-match handling, the two capped reference credits, model/panel details, execution settings and dates, and the full worked example.
- The original manuscript’s repository placeholder and anonymous template settings. No archive URL, author information, or journal requirement was invented.

## Verification and use

The article compiles with the included style, bibliography, and figure assets. The final build has no undefined references/citations or overfull-box warnings. The abstract, prompts, retained tabular data, three RQs, and aggregation equations were checked against the supplied source. The primary figure matches the supplied PDF pixel-for-pixel, and all revised pages were visually inspected.

Open `shortened_manuscript.tex` as the main document in Overleaf after uploading the editing package. The app’s native LaTeX preview did not compile this project; the included PDF was compiled successfully with the project dependencies using the available local LaTeX installation. The source remains editable.

The detailed changes are reviewable in `analysis_archive/revision.diff`; no original file was overwritten. Archive the supplementary analyses with the final research release so the shortened article’s references to accompanying analysis files remain accessible.
