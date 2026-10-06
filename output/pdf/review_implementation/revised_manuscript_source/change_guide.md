# Manuscript implementation and original-PDF change guide

28 September 2026. Target: unspecified AI/NLP journal.

All locations below refer to the grey printed margin numbers in the original 22-page `0_version_2.pdf`, not the revised PDF or PDF-extraction row numbers. Each page has two columns of margin numbers. Full-width figures and tables are located by their caption plus the nearby margin grid. Line ranges identify the affected passage; exact LaTeX snippets below define the replacement boundaries. Source-line numbers refer to the original `0_version_2.tex`. Preamble changes have no printed body line.

## What is implemented

The separate manuscript contains 38 tracked LaTeX edits, bibliography updates, a legible vector Figure 2, and accompanying source and statistical evidence. Original manuscript files and the workbook remain unchanged. The title, main RQ order, prompts, reference texts, main equations, reported point estimates, and primary RQ1 result are preserved. Descriptive judge checks remain after RQ1-RQ3.

The supplied workbook resolves the previous missing source-to-perspective mapping: all 80 summaries and all 80 explanations exactly match the evaluated reference set, and all 80 source cells contain information. Seventy-four contain URLs and six contain textual citations. This verifies provenance correspondence, not complete support for every claim. Seven specific source records still need author attention; they are listed below.

Your clarification is incorporated: topic matching began with Serbian topics; comparator inclusion was investigator-guided using broad WEIRD attributes, with Poland acknowledged as borderline; distinct stances were chosen from the linked research. No formal threshold, selection algorithm, or tier-coding procedure has been invented. Appendix D.9 and its main-text pointer are removed at your request. Original archived metadata and the verbatim generation prompt remain intact.

The new analysis reruns saved scores only. The original 16-topic model comparison gives 15 BH-adjusted significant contrasts; exact enumeration at the same unit also gives 15. Keeping the eight matched pairs together gives zero (minimum adjusted p = 0.08705357). This is a sensitivity to the inferential unit, not evidence of model equivalence. All model means are unchanged. The primary RQ1 test is unchanged.

## Three highest-impact changes

1. Reference construction and provenance: original p. 3, lines 268-288; source workbook and an exact 80-record ledger are now supplied.
2. Inferential-unit sensitivity: p. 7, lines 665-668, with methods at p. 6, 584-596 and p. 17, 1646-1671; both specifications are reported.
3. Calibrated claims: p. 5, 476-481; p. 11, 1023-1038; fixed panels, uncertainty bounds, and illustrative t-test power are described without unsupported guarantees.

## Applied edits with exact locations

Apply these only to the original source if merging manually. They are already present in `revised_manuscript.tex`. “Replace” means replace the exact old span with the exact new span; retained surrounding text is intentionally omitted. “Add” gives the preceding anchor. For the PDF, use the page, margin range, and quoted anchor together. Copy from the Markdown version or source file to avoid PDF soft wrapping.

### 01. Preamble hyperref

**Location:** No printed PDF line: preamble-only change; repairs internal links to floats. Original LaTeX lines 11-11.

**Reason:** Let the journal style load hyperref after float-related packages, preventing duplicate float destinations. **Type/status:** Editing / documented clarification. Review correction, applied.

**Delete this exact source span:**

```latex
\usepackage{hyperref}
```

### 02. Preamble cleveref

**Location:** No printed PDF line: preamble-only change; repairs internal links to floats. Original LaTeX lines 19-19.

**Reason:** Move cleveref after the style loads hyperref. **Type/status:** Editing / documented clarification. Review correction, applied.

**Delete this exact source span:**

```latex
\usepackage{cleveref}
```

### 03. Preamble style order

**Location:** No printed PDF line: preamble-only change; repairs internal links to floats. Original LaTeX lines 62-62.

**Reason:** Load cross-reference support in the correct order; no body text changes. **Type/status:** Editing / documented clarification. Review correction, applied.

**Replace this exact source span:**

```latex
\usepackage{tacl2021v1}
```

**With / insert:**

```latex
\usepackage{tacl2021v1}
\usepackage{cleveref}
```

### 04. Abstract

**Location:** original PDF p. 1, lines 029–033; original PDF p. 1, lines 035–037 Original LaTeX lines 166-166.

**Reason:** Name the interval procedure and identify the pooled agreement coefficient; all numbers remain unchanged. **Type/status:** Editing / documented clarification. Review correction, applied.

**PDF anchor:** “The mean WEIRD-minus-Serbian difference”

**Replace this exact source span:**

```latex
CI: $-10.3$ to $7.7$), and an exact one-sided Wilcoxon signed-rank test found no evidence for the hypothesised WEIRD advantage ($p=0.680$). Differences between individual pairs ($-16.9$ to $+19.1$ points) were much larger than the pooled difference. Judges agreed similarly on both sets of topics (Fleiss'
```

**With / insert:**

```latex
$t$-based CI: $-10.3$ to $7.7$), and an exact one-sided Wilcoxon signed-rank test found no evidence for the hypothesised WEIRD advantage ($p=0.680$). Differences between individual pairs ($-16.9$ to $+19.1$ points) were much larger than the pooled difference. Inter-judge agreement was similar across the two settings (pooled Fleiss'
```

### 05. Contributions

**Location:** original PDF p. 2, lines 128; bullets 129–141 Original LaTeX lines 194-194.

**Reason:** The list contains two contributions, not three. **Type/status:** Editing / documented clarification. Review correction, applied.

**PDF anchor:** “The paper makes three contributions:”

**Replace this exact source span:**

```latex
three
```

**With / insert:**

```latex
two
```

### 06. Superglue

**Location:** original PDF p. 2, lines 168–180 Original LaTeX lines 212-212.

**Reason:** Distinguish language-understanding resources from cultural-perspective benchmarks. **Type/status:** Editing / documented clarification. Review correction, applied.

**PDF anchor:** “The concentration of training, preference, and”

**Replace this exact source span:**

```latex
Culturally focused benchmarks also document uneven resource coverage, including for Serbian and other
```

**With / insert:**

```latex
Language-specific evaluation resources also remain unevenly developed. Serbian SuperGLUE addresses gaps in complex language-understanding evaluation for Serbian and motivates broader coverage of
```

### 07. Overtonbench

**Location:** original PDF p. 3, lines 206–213 Original LaTeX lines 220-220.

**Reason:** Make the measurement distinction and incremental contribution explicit. **Type/status:** Editing / documented clarification. Review correction, applied.

**PDF anchor:** “The closest benchmark is OvertonBench, which”

**Replace this exact source span:**

```latex
coverage of diverse positions and validates representation with people who hold those views \cite{poole-dayanBenchmarkingOvertonPluralism2025}. We share its focus on perspective coverage. Our study adds a matched comparison of WEIRD and Serbian controversies to reduce confounding between cultural setting and topic selection.
```

**With / insert:**

```latex
perspective coverage using viewpoint groups derived from human responses and ratings of how well model outputs represent participants' views \cite{poole-dayanBenchmarkingOvertonPluralism2025}. Our study instead measures recovery of fixed, externally documented reference perspectives in structurally matched WEIRD and Serbian controversies. The contribution is this matched comparison across settings; differences in reference construction and scoring preclude direct comparison of absolute scores between the two benchmarks.
```

### 08. Judge citation

**Location:** original PDF p. 3, lines 216–220 Original LaTeX lines 224-224.

**Reason:** Narrow the claim to the inspected evidence; remove the mismatched Chen citation explicitly. **Type/status:** Editing / documented clarification. Review correction, applied.

**PDF anchor:** “Evaluating coverage requires deciding whether”

**Replace this exact source span:**

```latex
semantic relationship, but their decisions may depend on presentation, style, and model provenance \cite{poole-dayanBenchmarkingOvertonPluralism2025, chenBenchmarkingLargeLanguage2025}.
```

**With / insert:**

```latex
relationship, but their agreement with human assessments can vary across the models being evaluated \cite{poole-dayanBenchmarkingOvertonPluralism2025}.
```

### 09. Weird scope

**Location:** original PDF p. 3, lines 257–265; especially 261–265 Original LaTeX lines 239-240.

**Reason:** Report the author-confirmed investigator-guided grouping and the acknowledged borderline inclusion of Poland, without inventing a formal classification rule. **Type/status:** Editing / documented clarification. Review correction, applied.

**PDF anchor:** “The procedure was investigator-guided rather”

**Replace this exact source span:**

```latex
Here, WEIRD and Serbian identify the two benchmark groups; Serbia is the single non-WEIRD setting studied. Matching reduces ambiguity due to topic selection without experimentally isolating cultural setting.
% AUTHOR CHECK: document the operational WEIRD inclusion rule; it was not recorded in the supplied project.
```

**With / insert:**

```latex
Comparator selection was guided by broad Western, educational, industrial and economic characteristics, rather than a quantified country-classification rule. WEIRD therefore labels the selected comparator populations in Table~\ref{tab:topics}; it is not a validated binary country classification or representative sampling of a cultural category. Poland was included as a borderline case under this investigator judgment. Matching reduces ambiguity due to topic selection without experimentally isolating cultural setting.
```

### 10. Source ledger

**Location:** original PDF p. 3, lines 268–288 Original LaTeX lines 265-265.

**Reason:** Replace the missing-source concern with the newly supplied workbook and an explicit provenance ledger. **Type/status:** Editing / documented clarification. Review correction, applied.

**PDF anchor:** “A reference perspective is a substantively distinct”

**Replace this exact source span:**

```latex
Every perspective is linked to its supporting sources, and these links will be released with the benchmark.
```

**With / insert:**

```latex
The first author selected five distinct stances per topic from the linked research and reporting. The source workbook records a source entry for each of the 80 reference perspectives. The accompanying source ledger links the evaluated reference identifiers to their workbook cells and preserves both the source text and any embedded hyperlink. All reference summaries and explanations in the workbook match the evaluated reference set exactly. Source entries identify the evidence used in construction; they do not imply that every clause of an advocate-style explanation is a quotation or a measured population belief.
```

### 11. Source language

**Location:** original PDF p. 3, lines 268–288 Original LaTeX lines 267-267.

**Reason:** Correct the unsupported blanket claim that all Serbian-topic sources are in Serbian. **Type/status:** Editing / documented clarification. Review correction, applied.

**PDF anchor:** “A reference perspective is a substantively distinct”

**Replace this exact source span:**

```latex
Sources for the Serbian topics are in Serbian, and the first author summarised them in English.
```

**With / insert:**

```latex
Reference summaries and explanations were written in English. Sources cited for Serbian topics include English-language research, reporting, and survey materials; the language of the cited material was therefore not uniformly Serbian.
```

### 12. Size groups

**Location:** original PDF p. 5, lines 422–426; exact note 425 Original LaTeX lines 300-300.

**Reason:** Remove the visible drafting note and define membership without inventing a parameter-count rule. **Type/status:** Editing / documented clarification. Review correction, applied.

**PDF anchor:** “Gemma 4 31B and Llama 3.3 70B are smaller only relative”

**Replace this exact source span:**

```latex
Gemma 4 31B and Llama 3.3 70B are smaller only relative to the other open-weight models in this selection, \textbf{[measured by total parameter count]}.
```

**With / insert:**

```latex
The smaller open-weight group consists of the two selected systems labelled 31B and 70B, Gemma 4 31B and Llama 3.3 70B; the other six open-weight systems form the larger group. These labels identify the groups used in this comparison rather than a general size taxonomy.
```

### 13. Panel protection

**Location:** original PDF p. 5, lines 476–481 Original LaTeX lines 340-340.

**Reason:** Replace an unjustified guarantee with the actual control provided by constant panel membership. **Type/status:** Editing / documented clarification. Review correction, applied.

**PDF anchor:** “Because a generator’s panel depends only on its developer”

**Replace this exact source span:**

```latex
Because a generator's panel depends only on its developer, each generator is judged by the same panel on its WEIRD and Serbian topics. Panel substitution therefore cannot create a within-model WEIRD--Serbian difference, but it can shift a model's overall recall relative to other models
```

**With / insert:**

```latex
Each generator is judged by the same panel on its WEIRD and Serbian topics, avoiding changes in panel membership between the two settings. This does not exclude topic-dependent or culturally differential judging errors. Differences between panels may also affect comparisons of overall recall between generators
```

### 14. Notation

**Location:** original PDF p. 6, lines 533–539; definitions 541–543 Original LaTeX lines 362-368.

**Reason:** Introduce model-summary symbols before their first equation; preserve the equation. **Type/status:** Editing / documented clarification. Optional presentation or compactness improvement, applied.

**PDF anchor:** “Step 3: summarise a model across topics.”

**Replace this exact source span:**

```latex
Overall model recall averages its $16$ model-topic scores; WEIRD and Serbian recall each average eight:
\begin{equation}
\overline R_m=\frac{1}{16}\sum_{t=1}^{16}R_{mt}
=\frac{\overline R_m^{\mathrm W}+\overline R_m^{\mathrm S}}{2}.
\label{eq:model-recall}
\end{equation}
Let $\overline R_m$ denote the model's overall recall, and let $\overline R_m^{\mathrm W}$ and $\overline R_m^{\mathrm S}$ denote its mean recall on WEIRD and Serbian topics, respectively.
```

**With / insert:**

```latex
Let $\overline R_m$ denote the model's overall recall, and let $\overline R_m^{\mathrm W}$ and $\overline R_m^{\mathrm S}$ denote its mean recall on WEIRD and Serbian topics, respectively. Overall model recall averages its $16$ model-topic scores; WEIRD and Serbian recall each average eight:
\begin{equation}
\overline R_m=\frac{1}{16}\sum_{t=1}^{16}R_{mt}
=\frac{\overline R_m^{\mathrm W}+\overline R_m^{\mathrm S}}{2}.
\label{eq:model-recall}
\end{equation}
```

### 15. Stats summary

**Location:** original PDF p. 6, lines 584–596 Original LaTeX lines 389-389.

**Reason:** Make the new existing-data sensitivity visible in the main methods. **Type/status:** Existing-data analysis and reporting. Review correction, applied.

**PDF anchor:** “RQ2: describe models and compare categories.”

**Replace this exact source span:**

```latex
(Appendix~\ref{app:category-tests}).
```

**With / insert:**

```latex
(Appendix~\ref{app:category-tests}). Pairwise model tests and model-level intervals are also checked using matched-pair blocks, because the individual-topic procedures do not retain the pairing (Appendices~\ref{app:model_pair_tests} and~\ref{app:bootstrap}).
```

### 16. Figure1 interval caption

**Location:** original PDF p. 8, lines graphic near 700–720 left / 750–770 right; caption 723–724 left / 773–774 right Original LaTeX lines 412-412.

**Reason:** Explicitly distinguish the displayed bootstrap interval from the t interval used in the abstract. **Type/status:** Editing / documented clarification. Review correction, applied.

**PDF anchor:** “Recall differences across eight matched topic pairs”

**Replace this exact source span:**

```latex
shown.}
```

**With / insert:**

```latex
shown. The $t$-based interval for the mean is reported in Section~\ref{sec:rq1}.}
```

### 17. Rq2 pairwise

**Location:** original PDF p. 7, lines 665–668 Original LaTeX lines 418-418.

**Reason:** Retain the historical result and add the verified pair-blocked sensitivity without claiming equivalence. **Type/status:** Existing-data analysis and reporting. Review correction, applied.

**PDF anchor:** “Of the 78 pairwise model comparisons, 15 remain significant”

**Replace this exact source span:**

```latex
(Appendix~\ref{app:pairwise_results}).
```

**With / insert:**

```latex
when the 16 topics are treated as separate sign-flip units. None remains significant when the eight matched pairs are retained as blocks (minimum adjusted $p=0.087$). The inferential result is therefore sensitive to the unit of analysis, although the mean differences are unchanged (Appendix~\ref{app:pairwise_results}).
```

### 18. Rq2 panel attribution

**Location:** original PDF p. 7, lines 690–699; causal sentence 696–699; original PDF p. 8, lines 748 Original LaTeX lines 453-453.

**Reason:** Avoid attributing a measured fraction of between-model differences to panels without identifying that effect. **Type/status:** Editing / documented clarification. Review correction, applied.

**PDF anchor:** “Judge panels also differ”

**Replace this exact source span:**

```latex
judge, so small recall differences between them and other models, such as Gemma 4 31B's closeness to GPT 5.5, partly reflect panel composition.
```

**With / insert:**

```latex
judge. Small recall differences between them and other models, such as Gemma 4 31B's closeness to GPT 5.5, should therefore be interpreted with this difference in panel composition in mind.
```

### 19. Rq3 effect

**Location:** original PDF p. 9, lines 801–814; especially 804–808 Original LaTeX lines 457-457.

**Reason:** Add the verified existing interval for overall recall and specify the subtraction order. **Type/status:** Existing-data analysis and reporting. Review correction, applied.

**PDF anchor:** “The four models from Chinese developers had”

**Replace this exact source span:**

```latex
groups differ in composition: only the US group includes the two smaller open-weight models, and excluding them reduces the
```

**With / insert:**

```latex
US-minus-China difference is $-0.030$ (95\% pair-bootstrap CI $[-0.048,-0.013]$). The groups differ in composition: only the US group includes the two smaller open-weight models, and excluding them reduces the magnitude of the US-minus-China
```

### 20. Rq3 duplicate

**Location:** original PDF p. 9, lines 832–834 Original LaTeX lines 475-475.

**Reason:** Remove the duplicated model-comparison result from the developer-country subsection. **Type/status:** Editing / documented clarification. Optional presentation or compactness improvement, applied.

**PDF anchor:** “Of the 78 pairwise model comparisons, 15 remain”

**Replace this exact source span:**

```latex
gap. Of the 78 pairwise model comparisons, 15 remain significant after Benjamini--Hochberg adjustment (Appendix~\ref{app:pairwise_results}).
```

**With / insert:**

```latex
gap.
```

### 21. Discussion duplicate

**Location:** original PDF p. 9, lines 884–886; retain preceding 878–883 Original LaTeX lines 508-508.

**Reason:** Delete the standalone sentence repeating the immediately preceding paragraph. **Type/status:** Editing / documented clarification. Optional presentation or compactness improvement, applied.

**PDF anchor:** “The primary comparison found no detectable”

**Delete this exact source span:**

```latex
The primary comparison found no detectable WEIRD recall advantage, while coverage remained incomplete in both settings.
```

### 22. Discussion categories

**Location:** original PDF p. 10, lines 933–937; original PDF p. 10, lines 938–940 Original LaTeX lines 523-523.

**Reason:** Limit the category interpretation to the selected models and remove the pointer to the author-withdrawn extremity analysis. **Type/status:** Editing / documented clarification. Review correction, applied.

**PDF anchor:** “Model performance also overlaps across access”

**Replace this exact source span:**

```latex
are therefore poor substitutes for measuring perspective coverage directly. Appendix~\ref{app:extremity} reports descriptive summaries of perspective extremity; these do not establish why coverage varies across topics.
```

**With / insert:**

```latex
did not reliably summarise the variation among the selected models.
```

### 23. Deliberation citation

**Location:** original PDF p. 10, lines 969–977; citations 973 Original LaTeX lines 533-533.

**Reason:** Remove DEBATE from the human-deliberation citation group; its evaluation setting differs. **Type/status:** Editing / documented clarification. Review correction, applied.

**PDF anchor:** “This distinction also matters for AI-mediated”

**Replace this exact source span:**

```latex
kimDEBATEDevilsAdvocateBased2024a, leeAmplifyingMinorityVoices2025a}.
```

**With / insert:**

```latex
leeAmplifyingMinorityVoices2025a}.
```

### 24. Reference limits language

**Location:** original PDF p. 10, lines 985–999; continues p11 1000–1002 Original LaTeX lines 541-541.

**Reason:** Propagate the corrected source-language description into the limitations. **Type/status:** Editing / documented clarification. Review correction, applied.

**PDF anchor:** “Each topic has five externally documented reference perspectives.”

**Replace this exact source span:**

```latex
Serbian-language sources, so
```

**With / insert:**

```latex
sources in more than one language, so summarisation and
```

### 25. Power and bound

**Location:** original PDF p. 11, lines 1023–1033; original PDF p. 11, lines 1034–1038 Original LaTeX lines 551-551.

**Reason:** Qualify the bound and correctly identify the power calculation; preserve reported numerical values. **Type/status:** Editing / documented clarification. Review correction, applied.

**PDF anchor:** “The primary comparison rests on eight topic pairs”

**Replace this exact source span:**

```latex
is likely to be too narrow; a $t$-based interval is $-10.3$ to $7.7$ points, and the one-sided 95\% upper bound is $5.9$ points. The data therefore argue against a WEIRD advantage much larger than about six points for pairs like these, but cannot exclude smaller advantages or moderate differences favouring Serbian topics. Given this between-pair variation, a one-sided test at $\alpha=0.05$ would detect a five-point WEIRD advantage only about one time in three, and reaches 80\% power only for advantages of about 10.5 points.
```

**With / insert:**

```latex
may have limited coverage accuracy; a $t$-based interval is $-10.3$ to $7.7$ points, and the one-sided 95\% upper bound is $5.9$ points. Under the independent-pair and $t$-interval assumptions, the one-sided bound is approximately six points. It is conditional on these assumptions and the selected benchmark; it does not establish a general upper bound on cultural disparities. Smaller WEIRD advantages and moderate differences favouring Serbian topics remain compatible with the interval. An illustrative sensitivity calculation for a one-sided one-sample $t$-test at $\alpha=0.05$, assuming normally distributed pair-level differences and using the observed SD, gives approximately 32\% power for a five-point WEIRD advantage and 80\% power for an advantage of about 10.5 points. These values describe the $t$-test calculation, not the exact Wilcoxon procedure used for the primary test.
```

### 26. Availability

**Location:** original PDF p. 11, lines 1096; paragraph 1098–1099; original PDF p. 12, lines 1100–1103 Original LaTeX lines 575-577.

**Reason:** Make the local review package concrete without fabricating a public repository URL. **Type/status:** Editing / documented clarification. Partly resolved; persistent archive identifier remains a submission action.

**PDF anchor:** “The accompanying source package contains the”

**Replace this exact source span:**

```latex
reference statements, model configurations, the worked-example record, and supplementary result tables. Generation and judgment logs and analysis code are maintained in the evaluation project.
% AUTHOR CHECK: insert the final public repository or archival URL. The supplied URL ended in REPOSITORY, and no git remote was configured.
% AUTHOR CHECK: include the external source-to-reference ledger before publication.
```

**With / insert:**

```latex
evaluated reference statements, original source workbook, reference-to-source ledger, model and judge configurations, worked-example record, and supplementary result tables. It also includes the saved model-topic scores and reproducible scripts for the additional matched-pair sensitivity analyses. The ledger preserves the workbook's source text and hyperlinks separately where they differ. The final repository or archival identifier will be added before submission.
% AUTHOR QUERY: deposit the final package and replace the final sentence with its actual persistent URL; resolve the source-ledger query list first.
```

### 27. Judge table reference

**Location:** original PDF p. 14, lines 1394–1399; original PDF p. 15, lines 1400–1402 Original LaTeX lines 708-708.

**Reason:** Add the missing explicit Table 7 citation. **Type/status:** Editing / documented clarification. Review correction, applied.

**PDF anchor:** “The base panel contains five judges from distinct”

**Replace this exact source span:**

```latex
panel.
```

**With / insert:**

```latex
panel. Table~\ref{tab:judge_substitutions} lists the substitutions.
```

### 28. Judge table layout

**Location:** original PDF p. 15, lines 1405–1409 Original LaTeX lines 714-726.

**Reason:** Wrap long table cells instead of shrinking the entire table. **Type/status:** Editing / documented clarification. Review correction, applied.

**PDF anchor:** “Table 7: Family-disjoint judge substitutions.”

**Replace this exact source span:**

```latex
\resizebox{\columnwidth}{!}{%
\begin{tabular}{lll}
\toprule
\textbf{Generator being evaluated} & \textbf{Base judge removed} & \textbf{Substitute} \\
\midrule
GPT 5.5 / GPT-OSS 120B & GPT 5.5 & Grok 4.5 \\
Claude Opus 4.8 & Claude Sonnet 5 & Grok 4.5 \\
Gemini 3.1 Pro / Gemma 4 31B & Gemini 3.1 Pro & Grok 4.5 \\
DeepSeek V4 Pro & DeepSeek V4 Pro & Qwen 3.7 Max \\
Kimi K2.6 & Kimi K2.6 & Grok 4.5 \\
\bottomrule
\end{tabular}%
}
```

**With / insert:**

```latex
\small
\begin{tabularx}{\columnwidth}{@{}Yp{0.25\columnwidth}p{0.20\columnwidth}@{}}
\toprule
Generator & Base judge removed & Substitute \\
\midrule
GPT 5.5 / GPT-OSS 120B & GPT 5.5 & Grok 4.5 \\
Claude Opus 4.8 & Claude Sonnet 5 & Grok 4.5 \\
Gemini 3.1 Pro / Gemma 4 31B & Gemini 3.1 Pro & Grok 4.5 \\
DeepSeek V4 Pro & DeepSeek V4 Pro & Qwen 3.7 Max \\
Kimi K2.6 & Kimi K2.6 & Grok 4.5 \\
\bottomrule
\end{tabularx}
```

### 29. Bootstrap details

**Location:** original PDF p. 16, lines 1516–1518; original PDF p. 16, lines 1519–1527; original PDF p. 16, lines 1527–1533 Original LaTeX lines 801-801.

**Reason:** Correct the interval label and document the new matched-pair model-interval sensitivity. **Type/status:** Existing-data analysis and reporting. Review correction, applied.

**PDF anchor:** “Model-level recall, precision, and F1 confidence”

**Replace this exact source span:**

```latex
reported primary interval is $[-0.08096,\,0.05823]$. The $t$-based interval for the mean gap uses the eight $\Delta_p$ values (SD $0.107$, SE $0.038$) with $t_{7}$ quantiles, giving $[-0.103, 0.077]$; the one-sided 95\% upper bound is $0.059$. Power uses the noncentral $t$ distribution with seven degrees of freedom and the observed between-pair SD: a five-point WEIRD advantage gives 32\% power, and 80\% power requires 10.5 points. These are sensitivity values for hypothetical effects, not power at the observed effect.
```

**With / insert:**

```latex
pair-bootstrap interval is $[-0.08096,\,0.05823]$. The $t$-based interval for the mean gap uses the eight $\Delta_p$ values (SD $0.107$, SE $0.038$) with $t_{7}$ quantiles, giving $[-0.103, 0.077]$; the one-sided 95\% upper bound is $0.059$. Power uses the noncentral $t$ distribution with seven degrees of freedom and the observed between-pair SD: a five-point WEIRD advantage gives 32\% power, and 80\% power requires 10.5 points. These are sensitivity values for hypothetical effects, not power at the observed effect. As a sensitivity analysis for each model, we also resample the eight matched pairs with replacement, retaining both topics of each pair and their equal weights. We use $10{,}000$ resamples and a fresh NumPy generator with seed $42$. The resulting intervals, alongside the original topic-bootstrap intervals, are supplied in \path{supplementary/model_pair_bootstrap_ci.csv}. This changes the resampling unit but not the model means.
```

### 30. Owen citation

**Location:** Original PDF p. 16, lines 1598-1599 (footnote 2); associated crossed-bootstrap paragraph in Appendix D.3. Original LaTeX lines 834-834.

**Reason:** Move the already identified Owen source from a footnote into the bibliography. **Type/status:** Editing / documented clarification. Review correction, applied.

**Replace this exact source span:**

```latex
$[-0.090,0.070]$.\footnote{The resampling scheme follows Owen (2007), \emph{The pigeonhole bootstrap}, \href{https://arxiv.org/abs/0712.1111}{arXiv:0712.1111}.}
```

**With / insert:**

```latex
$[-0.090,0.070]$. The resampling scheme follows \citet{owen2007pigeonhole}.
```

### 31. Pairwise details

**Location:** original PDF p. 17, lines 1646–1649; original PDF p. 17, lines 1651–1671 Original LaTeX lines 878-878.

**Reason:** Document the exact new sensitivity and its assumptions without silently replacing the original test. **Type/status:** Existing-data analysis and reporting. Review correction, applied.

**PDF anchor:** “D.6 Pairwise model comparisons”

**Replace this exact source span:**

```latex
patterns.
```

**With / insert:**

```latex
patterns.

The individual-topic sign-flip procedure assumes sign exchangeability at the topic level and does not preserve the matched pairs. To assess sensitivity to this choice, we also form eight pair-level contrasts,
\[
x_p=\frac{R_{a,p}^{\mathrm W}+R_{a,p}^{\mathrm S}}{2}
    -\frac{R_{b,p}^{\mathrm W}+R_{b,p}^{\mathrm S}}{2},
\]
and enumerate all $2^8=256$ sign assignments using their mean as the statistic. Two-sided tail comparisons allow a numerical tolerance of $10^{-12}$, and Benjamini--Hochberg correction again covers all $78$ model comparisons. This procedure assumes sign-exchangeable pair-level contrasts and preserves the original mean difference. As a numerical check, exhaustive enumeration of the $2^{16}$ individual-topic sign patterns still yields 15 adjusted significant comparisons, whereas the pair-blocked procedure yields none (minimum adjusted $p=0.087$). The discrepancy therefore reflects the inferential unit rather than Monte Carlo sampling alone. The pair-blocked results qualify the individual-topic findings; neither procedure establishes equivalence between models.
```

### 32. Remove extremity

**Location:** original PDF p. 18, lines 1708–1724; tier counts 1710–1715 Original LaTeX lines 898-906.

**Reason:** Remove Appendix D.9 and its counts/correlations at the author's explicit request. Original data remain archived; no main RQ result changes. **Type/status:** Editing / documented clarification. Review correction, applied.

**PDF anchor:** “D.9 Descriptive extremity analysis”

**Delete this exact source span:**

```latex
\subsection{Descriptive extremity analysis}
\label{app:extremity}

The $80$ reference perspectives contain $32$ perspectives tagged mainstream, $30$ tagged minority, and $18$ tagged extreme. The Serbian topics contain $18$ mainstream, $12$ minority, and $10$ extreme references; the WEIRD topics contain $14$ mainstream, $18$ minority, and $8$ extreme references.

Mean recovery is $0.593$ for mainstream perspectives, $0.650$ for minority perspectives, and $0.475$ for extreme perspectives. Across the $16$ topics, mean recall correlates weakly with the share of extreme references ($\rho=-0.127$) and the share of minority references ($\rho=-0.041$).

These summaries are descriptive. We report no inferential test of extremity differences or associations with topic-level recall, and they are not part of the primary hypothesis test.
% AUTHOR CHECK: document who assigned the tiers and the annotation criteria.
```

### 33. Figure2 legibility

**Location:** original PDF p. 19, lines graphic near 1800–1814 left / 1850–1864 right; caption 1816–1818 left / 1866–1868 right Original LaTeX lines 916-916.

**Reason:** Use a vector figure with larger labels and a two-row arrangement; preserve all three panels and the 104 scores. **Type/status:** Editing / documented clarification. Review correction, applied.

**PDF anchor:** “The same paired recalls, summarized at three levels”

**Replace this exact source span:**

```latex
\includegraphics[width=\textwidth]{plots/paired_recall.png}
```

**With / insert:**

```latex
\includegraphics[width=\textwidth]{plots/paired_recall.pdf}
```

The referenced `plots/paired_recall.pdf` is supplied in the source package; changing the filename alone is insufficient. It retains the same 104 cells and all three panels.

### 34. Pairwise results

**Location:** original PDF p. 18, lines 1744–1749 Original LaTeX lines 954-954.

**Reason:** Point readers to both inferential specifications and their results. **Type/status:** Existing-data analysis and reporting. Review correction, applied.

**PDF anchor:** “E.3 Pairwise model comparisons”

**Replace this exact source span:**

```latex
Appendix~\ref{app:model_pair_tests}.
```

**With / insert:**

```latex
Appendix~\ref{app:model_pair_tests}. The companion file \path{supplementary/pair_blocked_model_comparisons.csv} reports the individual-topic Monte Carlo results, exact individual-topic checks, and exact matched-pair results for the same comparisons. Mean recall differences are unchanged; 15 comparisons survive adjustment under the individual-topic procedures and none under pair blocking.
```

### 35. Per model table layout

**Location:** original PDF p. 20, lines 1916–1932 left; 1966–1982 right Original LaTeX lines 966-991.

**Reason:** Remove automatic enlargement of Table 9 while preserving all entries. **Type/status:** Editing / documented clarification. Review correction, applied.

**PDF anchor:** “Table 9: Per-model WEIRD-minus-Serbian recall comparisons.”

**Replace this exact source span:**

```latex
\resizebox{\textwidth}{!}{%
\begin{tabular}{lrrrrr}
\toprule
\textbf{Model} &
\textbf{Mean gap} &
\textbf{Median gap} &
\textbf{One-sided $p$} &
\textbf{Rank-biserial} &
\textbf{$p_{\mathrm{BH}}$} \\
\midrule
GLM 5.2 & $0.106$ & $0.100$ & $0.0625$ & $0.639$ & $0.6348$ \\
GPT-OSS 120B & $0.058$ & $0.100$ & $0.0977$ & $0.556$ & $0.6348$ \\
Llama 4 Maverick & $0.035$ & $-0.040$ & $0.4805$ & $0.056$ & $0.9445$ \\
Llama 3.3 70B & $0.015$ & $0.000$ & $0.4336$ & $0.111$ & $0.9445$ \\
DeepSeek V4 Pro & $0.010$ & $-0.020$ & $0.4688$ & $0.071$ & $0.9445$ \\
Kimi K2.6 & $-0.019$ & $0.000$ & $0.6875$ & $-0.200$ & $0.9445$ \\
GPT 5.5 & $-0.020$ & $0.020$ & $0.6523$ & $-0.139$ & $0.9445$ \\
Grok 4.3 & $-0.020$ & $-0.040$ & $0.6211$ & $-0.111$ & $0.9445$ \\
Mistral Large 3 & $-0.040$ & $-0.040$ & $0.7266$ & $-0.250$ & $0.9445$ \\
Gemini 3.1 Pro & $-0.045$ & $-0.020$ & $0.7188$ & $-0.222$ & $0.9445$ \\
Qwen 3.7 Max & $-0.073$ & $-0.100$ & $0.9375$ & $-0.583$ & $0.9688$ \\
Gemma 4 31B & $-0.082$ & $-0.100$ & $0.9688$ & $-0.810$ & $0.9688$ \\
Claude Opus 4.8 & $-0.095$ & $-0.180$ & $0.8555$ & $-0.417$ & $0.9688$ \\
\bottomrule
\end{tabular}%
}
```

**With / insert:**

```latex
\begin{tabular}{lrrrrr}
\toprule
\textbf{Model} &
\textbf{Mean gap} &
\textbf{Median gap} &
\textbf{One-sided $p$} &
\textbf{Rank-biserial} &
\textbf{$p_{\mathrm{BH}}$} \\
\midrule
GLM 5.2 & $0.106$ & $0.100$ & $0.0625$ & $0.639$ & $0.6348$ \\
GPT-OSS 120B & $0.058$ & $0.100$ & $0.0977$ & $0.556$ & $0.6348$ \\
Llama 4 Maverick & $0.035$ & $-0.040$ & $0.4805$ & $0.056$ & $0.9445$ \\
Llama 3.3 70B & $0.015$ & $0.000$ & $0.4336$ & $0.111$ & $0.9445$ \\
DeepSeek V4 Pro & $0.010$ & $-0.020$ & $0.4688$ & $0.071$ & $0.9445$ \\
Kimi K2.6 & $-0.019$ & $0.000$ & $0.6875$ & $-0.200$ & $0.9445$ \\
GPT 5.5 & $-0.020$ & $0.020$ & $0.6523$ & $-0.139$ & $0.9445$ \\
Grok 4.3 & $-0.020$ & $-0.040$ & $0.6211$ & $-0.111$ & $0.9445$ \\
Mistral Large 3 & $-0.040$ & $-0.040$ & $0.7266$ & $-0.250$ & $0.9445$ \\
Gemini 3.1 Pro & $-0.045$ & $-0.020$ & $0.7188$ & $-0.222$ & $0.9445$ \\
Qwen 3.7 Max & $-0.073$ & $-0.100$ & $0.9375$ & $-0.583$ & $0.9688$ \\
Gemma 4 31B & $-0.082$ & $-0.100$ & $0.9688$ & $-0.810$ & $0.9688$ \\
Claude Opus 4.8 & $-0.095$ & $-0.180$ & $0.8555$ & $-0.417$ & $0.9688$ \\
\bottomrule
\end{tabular}
```

### 36. Per model table reference

**Location:** original PDF p. 18, lines 1751–1754 Original LaTeX lines 994-994.

**Reason:** Add the missing explicit Table 9 citation. **Type/status:** Editing / documented clarification. Review correction, applied.

**PDF anchor:** “No individual generator has a one-sided raw p <”

**Replace this exact source span:**

```latex
No
```

**With / insert:**

```latex
Table~\ref{tab:per_model_weird_gap} reports the per-model comparisons. No
```

### 37. Worked tables layout

**Location:** original PDF p. 21, lines 2005–2021 left; original PDF p. 21, lines 2033–2044 left Original LaTeX lines 1040-1074.

**Reason:** Place the generated-summary table and assignment table side by side, retaining their separate captions and labels. **Type/status:** Editing / documented clarification. Optional presentation or compactness improvement, applied.

**PDF anchor:** “Table 10: The five generated summaries from GPT 5.5”

**Replace this exact source span:**

```latex
\begin{table}[htbp]
\centering\small
\caption{The five generated summaries from GPT 5.5 for UK fracking.}
\label{tab:fracking-outputs}
\begin{tabularx}{\columnwidth}{@{}rY@{}}
\toprule
Output & Summary \\
\midrule
1 & Fracking should be banned because it threatens the climate, countryside, water, and local communities. \\
2 & I oppose fracking mainly because I do not trust companies or government regulators to keep local people safe. \\
3 & The UK should frack because we need domestic gas for energy security, jobs, tax revenue, and lower reliance on imports. \\
4 & Fracking should be allowed only where geology supports it, regulation is strict, and local communities consent and benefit financially. \\
5 & We should embrace fracking and stop letting net-zero politics block cheap domestic energy. \\
\bottomrule
\end{tabularx}
\end{table}

\begin{table}[htbp]
\centering\small
\caption{Recorded assignments for the five GPT 5.5 outputs. A number identifies the matched reference; 0 denotes no match. Judge columns are Gemini 3.1 Pro (G), Claude Sonnet 5 (C), DeepSeek V4 Pro (D), Kimi K2.6 (K), and Grok 4.5 (X). All 25 judgments are valid.}
\label{tab:fracking-matches}
\begin{tabular}{@{}lrrrrr@{}}
\toprule
Output & G & C & D & K & X \\
\midrule
1 & 2 & 2 & 2 & 2 & 2 \\
2 & 0 & 2 & 0 & 0 & 0 \\
3 & 1 & 1 & 1 & 1 & 1 \\
4 & 5 & 5 & 5 & 5 & 0 \\
5 & 1 & 1 & 1 & 1 & 1 \\
\midrule
Judge recall & 0.60 & 0.60 & 0.60 & 0.60 & 0.40 \\
\bottomrule
\end{tabular}
\end{table}
```

**With / insert:**

```latex
\begin{table*}[!tp]
\begin{minipage}[t]{0.48\textwidth}
\centering\small
\caption{The five generated summaries from GPT 5.5 for UK fracking.}
\label{tab:fracking-outputs}
\begin{tabularx}{\columnwidth}{@{}rY@{}}
\toprule
Output & Summary \\
\midrule
1 & Fracking should be banned because it threatens the climate, countryside, water, and local communities. \\
2 & I oppose fracking mainly because I do not trust companies or government regulators to keep local people safe. \\
3 & The UK should frack because we need domestic gas for energy security, jobs, tax revenue, and lower reliance on imports. \\
4 & Fracking should be allowed only where geology supports it, regulation is strict, and local communities consent and benefit financially. \\
5 & We should embrace fracking and stop letting net-zero politics block cheap domestic energy. \\
\bottomrule
\end{tabularx}
\end{minipage}\hfill
\begin{minipage}[t]{0.48\textwidth}
\centering\small
\caption{Recorded assignments for the five GPT 5.5 outputs. A number identifies the matched reference; 0 denotes no match. Judge columns are Gemini 3.1 Pro (G), Claude Sonnet 5 (C), DeepSeek V4 Pro (D), Kimi K2.6 (K), and Grok 4.5 (X). All 25 judgments are valid.}
\label{tab:fracking-matches}
\begin{tabular}{@{}lrrrrr@{}}
\toprule
Output & G & C & D & K & X \\
\midrule
1 & 2 & 2 & 2 & 2 & 2 \\
2 & 0 & 2 & 0 & 0 & 0 \\
3 & 1 & 1 & 1 & 1 & 1 \\
4 & 5 & 5 & 5 & 5 & 0 \\
5 & 1 & 1 & 1 & 1 & 1 \\
\midrule
Judge recall & 0.60 & 0.60 & 0.60 & 0.60 & 0.40 \\
\bottomrule
\end{tabular}
\end{minipage}
\end{table*}
```

### 38. Identifier table layout

**Location:** original PDF p. 22, lines 2118–2131 left; 2168–2181 right Original LaTeX lines 1092-1092.

**Reason:** Allow the endpoint table to share the appendix float page with the worked-example tables. **Type/status:** Editing / documented clarification. Optional presentation or compactness improvement, applied.

**PDF anchor:** “Table 12: Configured identifiers for the evaluated generators.”

**Replace this exact source span:**

```latex
\begin{table*}[t]
```

**With / insert:**

```latex
\begin{table*}[!tp]
```

## Bibliography and added files

### B1. Sorensen publication details

**Location:** Original p. 13, lines 1229-1233; anchor “Taylor Sorensen, Jared Moore, Jillian Fisher”. Replace the provisional preprint record with the inspected ICML/PMLR publication record, retaining its citation key.

```bibtex
@inproceedings{sorensenRoadmapPluralisticAlignment2024,
  title = {Position: A Roadmap to Pluralistic Alignment},
  author = {Sorensen, Taylor and Moore, Jared and Fisher, Jillian and Gordon, Mitchell L. and Mireshghallah, Niloofar and Rytting, Christopher Michael and Ye, Andre and Jiang, Liwei and Lu, Ximing and Dziri, Nouha and Althoff, Tim and Choi, Yejin},
  booktitle = {Proceedings of the 41st International Conference on Machine Learning},
  pages = {46280--46302},
  year = {2024},
  volume = {235},
  series = {Proceedings of Machine Learning Research},
  publisher = {PMLR},
  url = {https://proceedings.mlr.press/v235/sorensen24a.html}
}
```

### B2. Owen bibliography entry

**Location:** Original p. 16, lines 1598-1599, footnote 2. Add the bibliographic record below. The corresponding text edit removes the manual footnote and uses the citation key. There is no original bibliography line for this new entry.

```bibtex
@article{owen2007pigeonhole,
  author = {Owen, Art B.},
  title = {The pigeonhole bootstrap},
  journal = {The Annals of Applied Statistics},
  year = {2007},
  volume = {1},
  number = {2},
  pages = {386--411},
  doi = {10.1214/07-AOAS122}
}
```

### B3. Removed in-text citations and corrected unused metadata

The Chen citation is removed at original p. 3, line 220 (see the judge-citation edit above); its rendered reference at p. 12, lines 1130-1139 disappears automatically after BibTeX because it is no longer cited. The retained database record corrects `pages = {10091--10109}` to `pages = {10080--10098}`. This is an explicit metadata correction, not a new citation. The Kim/DEBATE citation is removed at p. 10, line 973; its entry at p. 12, lines 1182-1188 likewise disappears from the rendered reference list. Do not manually edit the generated `.bbl`. Both unused database records remain available.

### S1. Source supplement

**Insertion location:** original p. 3, lines 277-279 and p. 11, lines 1098-1099 through p. 12, lines 1100-1103. Those passages already point to the accompanying source package after edits. Add the supplied original workbook, `source_provenance_ledger.csv` / `.json`, `source_urls.csv`, and `SOURCE_AUDIT.md` as supplementary files. A supplement itself has no original PDF line number. The extractor in `analysis/extract_sources.py` verifies the exact 80-record correspondence. Original source strings and conflicting native hyperlink targets are preserved separately.

### S2. Statistical supplement

**Insertion locations:** original p. 16, lines 1516-1533 and p. 18, lines 1744-1749. Add the supplied pair-blocked comparison CSV, model-pair bootstrap CSV, saved analysis inputs, and `analysis/reproduce_sensitivity.py`. The script verifies all 13 original intervals within 1e-12, all 78 unchanged mean differences, the exact sign-flip counts, and the saved RQ3 overall-recall interval. The new paired intervals are wider for six models and narrower for seven; do not claim that blocking necessarily widens them.

## Remaining author actions

These are unresolved evidence or submission details, not edits that can be invented. The current copy is a revised review draft, not a claim of final submission readiness.

| Reference | Workbook location | Evidence | Required action |
|---|---|---|---|
| Catalan independence p5 (`pair02_weird_p5`) | `01_WEIRD!P3` | Visible URL is a Converses a Catalunya article; native hyperlink points to a ResearchGate review of Kathryn Crameri's book. | Specify the intended source(s), preserve both in the working ledger, and identify the supporting passage. |
| Fracking p4 (`pair03_weird_p4`) | `01_WEIRD!M4` | Visible URL is an ECIU poll about MPs and net zero; native hyperlink points to the DESNZ renewable-energy report. | Resolve the link conflict and provide direct support for the reference's categorical anti-fracking stance. The cited DESNZ renewable report does not discuss shale gas/fracking. |
| Kosovo p3 (`pair02_serbian_p3`) | `02_Serbian!J3` | Visible Balkan Insight URL concerns Thaci's proposed border correction; native hyperlink points to a different article, “history's shadow.” | Specify the intended article(s) and support for the stance being held by people in Serbia. |
| Orbán p1 (`pair07_weird_p1`) | `01_WEIRD!D8` | A private Claude conversation is recorded as the source. Its displayed text fragment contains an encoded Magyar Nemzet URL. | Supply the underlying public document and supporting passage. The decoded public candidate was opened and concerns border protection, but full support for this reference remains unresolved; the original source is not silently replaced. |
| Kosovo p4 (`pair02_serbian_p4`) | `02_Serbian!M3` (explanation/summary `K3:L3`) | Broad references to HLC reports, named public intellectuals, and a foreign-policy-priority percentage; no identified HLC report or passage. Cells are red in the original workbook, without a legend. | Provide exact source titles/pages/URLs establishing the particular recognition/apology stance. A statistic about EU foreign-policy priority alone does not establish prevalence of this specific Kosovo stance. |
| Migrants p5 (`pair06_serbian_p5`) | `02_Serbian!P7` (explanation/summary `N7:O7`) | General references to party programmes and CRTA 2023–2024 media monitoring; no exact programme/report/passage. Original cells are red, without explanation. | Identify the exact documents and passages for the stated conspiratorial position. Do not infer why the cells were coloured red. |
| Fracking p5 (`pair03_weird_p5`) | `01_WEIRD!P4` | The sole listed URL is the DESNZ renewable-energy report; the benchmark statement is conditional support for shale gas. | Supply a fracking-specific source and a supporting passage. Do not replace the reference or recompute outcomes merely to repair a citation without an author decision. |


**Manuscript locations for all seven source queries:** original p. 3, lines 268-288 (construction and provenance) and p. 10, lines 985-999 through p. 11, lines 1000-1002 (scope of the reference set). The individual records occur in the workbook/supplement, so their exact actionable locators are sheet and cell, not invented PDF lines. For fracking p4/p5, also locate Table 2 on original p. 4, identified by the caption “Reference summaries for UK fracking”. Resolve the ledger entries first. If support is found, retain benchmark text and results. If an evaluated stance must change, that is a benchmark change requiring an explicit decision about affected scores and analyses; a new citation alone does not authorize changing it.

1. **Persistent access:** original p. 11, 1098-1099 through p. 12, 1100-1103. Deposit the final package and replace “The final repository or archival identifier will be added before submission.” with “The benchmark, source ledger, saved scores, and analysis code are available at [actual persistent URL].” This sentence is a template only until the real URL exists. Local files are provided; nothing was published. This remains a submission blocker.

2. **Author and venue information:** no target journal was specified. Venue-specific word/page limits, author statements, and anonymity requirements remain unverified. The PDF uses a TACL review template; that does not establish TACL as the intended journal. Check the acknowledgment at original p. 12, lines 1105-1111 against the chosen venue. The original hidden template-author fields have no printed PDF line and must be replaced with real author-supplied metadata for a non-anonymous version. Do not invent funding, ethics, conflict-of-interest, or contribution declarations.

3. **Generation and judgment archive:** the portable package supplies saved topic scores, configurations, and new-analysis inputs, not a complete API rerun environment or raw generation/judgment logs. The availability sentence has been limited accordingly. If the submission will claim full end-to-end reproducibility, include the existing raw logs and original pipeline in the final archive and document their execution. No new experiments are required for this packaging action.

## Optional work deliberately not presented as completed

Appendix D.8 (original p. 17, lines 1693-1699 through p. 18, 1700-1707) remains as a labelled descriptive sensitivity. Removing it is an optional compactness choice, unlike the author-requested deletion of D.9. Its existing caveats and cross-references remain. No further deletion is necessary for the present RQ argument.

Human judge validation is not fabricated. The manuscript already states this limitation at original p. 11, lines 1006-1019, and the calibrated claims remain conditional on the evaluation procedure. A stratified human audit would support stronger validity claims; it is not imposed as an arbitrary new experiment for the current conditional findings. Likewise, extra countries, models, prompts, or generation repeats would expand the study rather than repair the implemented writing changes.

## Verification and limits

The revised manuscript compiled with no unresolved references, overfull boxes, or duplicate hyperlink destinations. All 22 rendered manuscript pages were inspected. Source hashing confirms that the original manuscript and workbook were not edited. The 80-record text correspondence and additional statistics were checked programmatically; no new model generations or judgments were collected, and data authenticity was not established.

Only four workbook-related public pages received bounded live inspection: the UNDP migration publication page, two DESNZ Spring 2024 pages (renewables; energy infrastructure and security), and the Magyar Nemzet candidate decoded from the private-chat link. Their exact links and the limits of each check are in `supplementary/SOURCE_AUDIT.md`. This is not a claim to have authenticated all 80 underlying sources. The earlier citation audit also inspected the relevant OvertonBench, Serbian SuperGLUE, Chen, DEBATE, Sorensen, and Owen records/content used for the specific editorial corrections; it was not a verification of every cited article.

The unresolved source records and archive/venue details above remain author actions. Everything that can be implemented from the supplied materials is integrated in a separate source copy; unsupported details have not been guessed.
