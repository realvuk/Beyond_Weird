# Complete LaTeX swaps: original paper to shortened Fleiss-kappa revision

This file contains **every text change** between your original paper and the completed shortened revision. Nothing is abbreviated: each “Replace this” block is the exact original text, and each “With this” block is the complete replacement.

- **Original:** [0_version_2.tex](/Users/vuk/Downloads/0_version_2.tex).
- **Target:** [shortened_manuscript.tex](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex).
- **Scope:** 18 replacement blocks covering all 53 changed runs of lines. Nearby unchanged lines are included where useful to give a reliable search target.

## How to apply the swaps

1. Make a working copy of the original `.tex` file.
2. Follow the swaps below in order, from **Swap 01 to Swap 18**. They run from the bottom of the source towards the top, so the original line numbers for the remaining swaps stay valid.
3. In each step, replace the **entire** “Replace this” block, including the displayed headings, labels, environments, and blank lines, with the **entire** “With this” block. The LaTeX code blocks contain no added line-number prefixes.
4. Use the exact old text as a search anchor if your editor displays different line numbers. These line numbers apply to the original supplied `.tex`, not to PDF margin lines or an already edited copy.
5. Apply all swaps before compiling; some swaps move material that another swap removes. No other edits to the original `.tex` are needed to reproduce the shortened version.

The retained methods are one-sided Wilcoxon, two-sided sign-flip tests, Holm correction, and Fleiss’ kappa. Kappa’s reported values are **0.768 overall, 0.761 WEIRD, and 0.774 Serbian**; the replacements update the values as well as the coefficient’s name. All three research questions remain unchanged.

Material moved out of the article is preserved in [ANALYSIS_SUPPLEMENT.md](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/ANALYSIS_SUPPLEMENT.md), the `supplementary/` folder, and the original-source archive. Keep these with the revision. The swaps change the `.tex` text only; retain the supplied/current figure assets and bibliography. The [complete editing package](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision.zip) contains the dependencies used for the checked PDF.

## Swap index — apply in this order

| Swap | Original lines | Revised lines | Change |
|---|---|---|---|
| 01 | [1155–1159](/Users/vuk/Downloads/0_version_2.tex:1155) | [810–814](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:810) | Update the location of generator and judge configurations |
| 02 | [1130–1152](/Users/vuk/Downloads/0_version_2.tex:1130) | [785–807](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:785) | Add developer names to the model-identifier table |
| 03 | [1070–1073](/Users/vuk/Downloads/0_version_2.tex:1070) | [708–728](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:708) | Insert the unchanged fracking reference table beside the worked example |
| 04 | [887–1058](/Users/vuk/Downloads/0_version_2.tex:887) | [681–696](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:681) | Remove detailed secondary tests and agreement measures; retain kappa and judge-removal checks |
| 05 | [858–875](/Users/vuk/Downloads/0_version_2.tex:858) | [665–669](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:665) | Move alternative aggregation and crossed-model checks to the analysis files |
| 06 | [823–834](/Users/vuk/Downloads/0_version_2.tex:823) | [637–641](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:637) | Move additional intervals and the power calculation to the analysis files |
| 07 | [777–817](/Users/vuk/Downloads/0_version_2.tex:777) | [617–631](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:617) | Merge missing-data details and move precision/F1 definitions |
| 08 | [724–727](/Users/vuk/Downloads/0_version_2.tex:724) | [563–567](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:563) | Preserve developer-family definitions in Appendix C |
| 09 | [599–603](/Users/vuk/Downloads/0_version_2.tex:599) | [438–442](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:438) | Describe the accompanying analysis archive |
| 10 | [512–595](/Users/vuk/Downloads/0_version_2.tex:512) | [400–434](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:400) | Replace alpha results with kappa; condense discussion and limitations |
| 11 | [449–458](/Users/vuk/Downloads/0_version_2.tex:449) | [337–346](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:337) | Retain the model-comparison qualification and update the table caption |
| 12 | [438–442](/Users/vuk/Downloads/0_version_2.tex:438) | [326–330](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:326) | Update the RQ1 pointers to supplementary material |
| 13 | [429–433](/Users/vuk/Downloads/0_version_2.tex:429) | [317–321](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:317) | Use Fleiss’ kappa in the statistical methods |
| 14 | [421–425](/Users/vuk/Downloads/0_version_2.tex:421) | [309–313](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:309) | Make individual-model comparisons descriptive |
| 15 | [293–406](/Users/vuk/Downloads/0_version_2.tex:293) | [260–294](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:260) | Shorten generation, judging, and recall; remove the duplicate model table |
| 16 | [262–289](/Users/vuk/Downloads/0_version_2.tex:262) | [250–256](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:250) | Shorten reference construction and remove the main-text fracking table |
| 17 | [202–228](/Users/vuk/Downloads/0_version_2.tex:202) | [202–216](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:202) | Condense related work |
| 18 | [188–192](/Users/vuk/Downloads/0_version_2.tex:188) | [188–192](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:188) | Redirect supplementary precision and F1 reporting |

## Swap 01 — Update the location of generator and judge configurations

**Original lines:** [1155–1159](/Users/vuk/Downloads/0_version_2.tex:1155). **Revised lines:** [810–814](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:810).

### Replace this

````latex
The saved generation file contains $208$ unique model-topic responses and $1{,}040$ perspectives. The prompt allowed one to five perspectives, but every retained response contains five. One retained response does not imply one API request: failed requests could be retried and malformed JSON could receive a repair request. Saved generation timestamps span 9-10 July 2026 UTC. Judgment timestamps, including retries, span 10-20 July 2026 UTC.

Table~\ref{tab:model-identifiers} gives the configured endpoint identifiers. The GitHub repository includes the original generator and judge configurations. The judge configuration also identifies Claude Sonnet 5 as \path{anthropic/claude-sonnet-5} and the Grok substitute as \path{x-ai/grok-4.5}.

The release sources used for the public-weight categories are the published pages for \href{https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro}{DeepSeek V4 Pro}, \href{https://huggingface.co/moonshotai/Kimi-K2.6}{Kimi K2.6}, \href{https://huggingface.co/zai-org/GLM-5.2}{GLM 5.2}, \href{https://huggingface.co/collections/mistralai/mistral-large-3}{Mistral Large 3}, \href{https://ai.meta.com/llama/get-started/}{Meta's Llama models}, \href{https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/}{Gemma 4}, and \href{https://huggingface.co/openai/gpt-oss-120b}{GPT-OSS 120B}. The smaller group contains the selected 31B and 70B systems; the label is relative to the larger public-weight systems in this selection. It does not imply a common active-parameter count, runtime cost, licence, or training-data disclosure.
````

### With this

````latex
The saved generation file contains $208$ unique model-topic responses and $1{,}040$ perspectives. The prompt allowed one to five perspectives, but every retained response contains five. One retained response does not imply one API request: failed requests could be retried and malformed JSON could receive a repair request. Saved generation timestamps span 9-10 July 2026 UTC. Judgment timestamps, including retries, span 10-20 July 2026 UTC.

Table~\ref{tab:model-identifiers} gives the configured endpoint identifiers. The accompanying analysis files include the original generator and judge configurations. The judge configuration also identifies Claude Sonnet 5 as \path{anthropic/claude-sonnet-5} and the Grok substitute as \path{x-ai/grok-4.5}.

The release sources used for the public-weight categories are the published pages for \href{https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro}{DeepSeek V4 Pro}, \href{https://huggingface.co/moonshotai/Kimi-K2.6}{Kimi K2.6}, \href{https://huggingface.co/zai-org/GLM-5.2}{GLM 5.2}, \href{https://huggingface.co/collections/mistralai/mistral-large-3}{Mistral Large 3}, \href{https://ai.meta.com/llama/get-started/}{Meta's Llama models}, \href{https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/}{Gemma 4}, and \href{https://huggingface.co/openai/gpt-oss-120b}{GPT-OSS 120B}. The smaller group contains the selected 31B and 70B systems; the label is relative to the larger public-weight systems in this selection. It does not imply a common active-parameter count, runtime cost, licence, or training-data disclosure.
````

## Swap 02 — Add developer names to the model-identifier table

**Original lines:** [1130–1152](/Users/vuk/Downloads/0_version_2.tex:1130). **Revised lines:** [785–807](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:785).

### Replace this

````latex
\begin{table*}[!tp]
\centering\small
\caption{Configured identifiers for the evaluated generators.}
\label{tab:model-identifiers}
\begin{tabularx}{\textwidth}{@{}>{\raggedright\arraybackslash}p{0.26\textwidth}Y@{}}
\toprule
Model & Configured endpoint\\
\midrule
Claude Opus 4.8 & \path{anthropic/claude-opus-4.8}\\
GPT 5.5 & \path{openai/gpt-5.5}\\
Gemini 3.1 Pro & \path{google/gemini-3.1-pro-preview}\\
Grok 4.3 & \path{x-ai/grok-4.3}\\
DeepSeek V4 Pro & \path{deepseek/deepseek-v4-pro}\\
Qwen 3.7 Max & \path{qwen/qwen3.7-max}\\
Kimi K2.6 & \path{moonshotai/kimi-k2.6}\\
GLM 5.2 & \path{z-ai/glm-5.2}\\
Llama 4 Maverick & \path{meta-llama/llama-4-maverick}\\
Mistral Large 3 & \path{mistralai/mistral-large-2512}\\
GPT-OSS 120B & \path{openai/gpt-oss-120b}\\
Gemma 4 31B & \path{google/gemma-4-31b-it}\\
Llama 3.3 70B & \path{meta-llama/llama-3.3-70b-instruct}\\
\bottomrule
\end{tabularx}
````

### With this

````latex
\begin{table*}[!tp]
\centering\small
\caption{Developer mappings and configured identifiers for the evaluated generators. Category membership appears in Table~\ref{tab:model-recall}.}
\label{tab:model-identifiers}
\begin{tabularx}{\textwidth}{@{}>{\raggedright\arraybackslash}p{0.22\textwidth}lY@{}}
\toprule
Model & Developer & Configured endpoint\\
\midrule
Claude Opus 4.8 & Anthropic & \path{anthropic/claude-opus-4.8}\\
GPT 5.5 & OpenAI & \path{openai/gpt-5.5}\\
Gemini 3.1 Pro & Google & \path{google/gemini-3.1-pro-preview}\\
Grok 4.3 & xAI & \path{x-ai/grok-4.3}\\
DeepSeek V4 Pro & DeepSeek & \path{deepseek/deepseek-v4-pro}\\
Qwen 3.7 Max & Alibaba & \path{qwen/qwen3.7-max}\\
Kimi K2.6 & Moonshot & \path{moonshotai/kimi-k2.6}\\
GLM 5.2 & Z.AI & \path{z-ai/glm-5.2}\\
Llama 4 Maverick & Meta & \path{meta-llama/llama-4-maverick}\\
Mistral Large 3 & Mistral & \path{mistralai/mistral-large-2512}\\
GPT-OSS 120B & OpenAI & \path{openai/gpt-oss-120b}\\
Gemma 4 31B & Google & \path{google/gemma-4-31b-it}\\
Llama 3.3 70B & Meta & \path{meta-llama/llama-3.3-70b-instruct}\\
\bottomrule
\end{tabularx}
````

## Swap 03 — Insert the unchanged fracking reference table beside the worked example

**Original lines:** [1070–1073](/Users/vuk/Downloads/0_version_2.tex:1070). **Revised lines:** [708–728](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:708).

### Replace this

````latex
\label{app:worked-example}
This example follows one saved GPT 5.5 response to the topic \emph{UK fracking / shale gas}, with the reference population specified as ``people in the United Kingdom''. Tables~\ref{tab:reference-example} and~\ref{tab:fracking-outputs} reproduce the five reference summaries and generated summaries. Each perspective also has an explanation, which the judges received alongside its summary. The numerical assignments in Table~\ref{tab:fracking-matches} are the recorded judge decisions.

\begin{table*}[!tp]
````

### With this

````latex
\label{app:worked-example}
This example follows one saved GPT 5.5 response to the topic \emph{UK fracking / shale gas}, with the reference population specified as ``people in the United Kingdom''. Tables~\ref{tab:reference-example} and~\ref{tab:fracking-outputs} reproduce the five reference summaries and generated summaries. Each perspective also has an explanation, which the judges received alongside its summary. The numerical assignments in Table~\ref{tab:fracking-matches} are the recorded judge decisions.

\begin{table}[t]
\centering\small
\caption{Reference summaries for UK fracking, reproduced from the benchmark. The target population is ``people in the United Kingdom''. Each record also contains an explanation.}
\label{tab:reference-example}
\begin{tabularx}{\columnwidth}{@{}rY@{}}
\toprule
ID & Reference summary \\
\midrule
1 & Restart UK fracking for energy security and jobs. \\
2 & Ban fracking permanently on environmental and seismic grounds. \\
3 & Support fracking in principle but oppose it locally. \\
4 & Reject fracking categorically on climate-emergency grounds. \\
5 & Conditional pragmatist, support shale gas only with strict guarantees and a transition plan. \\
\bottomrule
\end{tabularx}
\end{table}

\begin{table*}[!tp]
````

## Swap 04 — Remove detailed secondary tests and agreement measures; retain kappa and judge-removal checks

**Original lines:** [887–1058](/Users/vuk/Downloads/0_version_2.tex:887). **Revised lines:** [681–696](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:681).

### Replace this

````latex
For overall recall, the US-minus-China difference is $-0.030$ ($95\%$ CI $[-0.048,-0.013]$), with raw $p=0.023$ and Holm-adjusted $p=0.047$. For the cultural gap, the difference is $-0.025$ ($95\%$ CI $[-0.082,0.025]$), with raw and adjusted $p=0.453$. These outcomes answer different questions: an overall recall difference does not establish a difference in the WEIRD-Serbian gap. The accompanying analysis files contain both contrasts and their uncertainty estimates.

\subsection{Pairwise model comparisons}
\label{app:model_pair_tests}

Pairwise model tests compare recall across the $16$ topics. For models $a$ and $b$, let $d_i=R_{a,i}-R_{b,i}$ for topic $i$. The observed statistic is

\begin{equation}
 T_{\mathrm{obs}}=\frac{1}{16}\sum_i d_i.
\end{equation}

For each model pair, the analysis samples $10,000$ random sign vectors $s_i\in\{-1,+1\}$ and computes

\begin{equation}
 T_s=\frac{1}{16}\sum_i s_i d_i.
\end{equation}

The test is two-sided. The Monte Carlo $p$-value is

\begin{equation}
 p=\frac{1+\#\{|T_s|\geq|T_{\mathrm{obs}}|\}}{10{,}001}.
\end{equation}

The random-number generator is initialized with seed $42$. All $\binom{13}{2}=78$ model pairs use this procedure, and the resulting raw $p$-values are adjusted jointly using the Benjamini-Hochberg procedure. This is a Monte Carlo paired sign-flip test, not exhaustive enumeration of all $2^{16}$ sign patterns.

The individual-topic sign-flip procedure assumes sign exchangeability at the topic level and does not preserve the matched pairs. To assess sensitivity to this choice, we also form eight pair-level contrasts,
\[
x_p=\frac{R_{a,p}^{\mathrm W}+R_{a,p}^{\mathrm S}}{2}
-\frac{R_{b,p}^{\mathrm W}+R_{b,p}^{\mathrm S}}{2},
\]
and enumerate all $2^8=256$ sign assignments using their mean as the statistic. Two-sided tail comparisons allow a numerical tolerance of $10^{-12}$, and Benjamini--Hochberg correction again covers all $78$ model comparisons. This procedure assumes sign-exchangeable pair-level contrasts and preserves the original mean difference. As a numerical check, exhaustive enumeration of the $2^{16}$ individual-topic sign patterns still yields 15 adjusted significant comparisons, whereas the pair-blocked procedure yields none (minimum adjusted $p=0.087$). The discrepancy therefore reflects the inferential unit rather than Monte Carlo sampling alone. The pair-blocked results qualify the individual topic findings; neither procedure establishes equivalence between models

\subsection{Per-model WEIRD-Serbian tests}
\label{app:per_model_tests}

The WEIRD-Serbian comparison is also repeated separately for each generator using its eight matched differences. Some generators contain zero differences or tied absolute differences. Differences read from the analysis files are therefore rounded to $12$ decimal places to remove negligible floating-point representation noise. Exact zeros are dropped, and the remaining absolute differences receive midranks.

For the $n$ remaining non-zero differences, all $2^n$ sign assignments are enumerated. For each assignment, the positive-rank sum $W^+$ is calculated. The directional $p$-value is

\begin{equation}
 P\left(W^+_{\mathrm{null}}\geq W^+_{\mathrm{obs}}\right).
\end{equation}

Rank-biserial correlation is calculated from the same signed ranks. The $13$ resulting $p$-values are adjusted using Benjamini-Hochberg.

\subsection{Per-reference mixed-effects check}
\label{app:mixed_model}

A separate robustness check fits a mixed-effects model to the $1,040$ per-reference recall-credit observations. Cultural arm is entered as a fixed effect, with random intercepts for matched pair and generator. The estimated WEIRD coefficient is $\beta_{\mathrm{WEIRD}}=-0.0131$ ($SE=0.0268$, $p=0.626$), consistent with the primary matched-pair analysis. This specification uses per-reference credits, whereas Appendix~\ref{app:gap-sensitivity} models $104$ model-pair differences. The two results come from different observational units and must not be interchanged. The per-reference specification does not explicitly model all dependence among references within a model-topic response.

\section{Secondary results}
\label{app:secondary_results}

\subsection{Paired recall at three levels}
\label{app:paired-views}
Figure~\ref{fig:paired-detail} shows the same paired scores at the topic-pair, model, and individual-cell levels. It complements the primary difference plot in Figure~\ref{fig:paired-recall}. The $104$ cells share generators and matched pairs; they are descriptive observations rather than independent replicates.
\begin{figure*}[t]
\centering
\includegraphics[width=\textwidth]{plots/paired_recall.png}
\caption{Paired recall at three levels. Panel A averages the $13$ generators within each matched topic pair. Panel B averages the eight pairs within each generator. Panel C plots all $104$ model-pair comparisons, with the dashed line indicating equal recall. Points above the line favour WEIRD topics. Panel C is descriptive: its observations share generators and matched topic pairs and are not independent replicates.}
\label{fig:paired-detail}
\end{figure*}

\subsection{Supplementary precision and F1}
\label{app:prf-results}
Table~\ref{tab:prf-supplement} preserves the model-level recall intervals and supplementary precision and F1 summaries from the saved analysis. Recall remains the primary outcome. F1 is the harmonic mean of model-level precision and recall, not an average of topic-level F1 scores. The displayed intervals use the original $10{,}000$-resample individual-topic bootstrap. Appendix~\ref{app:bootstrap} explains its distinction from the matched-pair recall sensitivity analysis supplied with the accompanying files. An unmatched output may express a legitimate position outside the reference set.

\begin{table*}[t]
\centering\small
\caption{Supplementary metrics with $95$\% bootstrap intervals, reproduced from the saved analysis. Rows are ordered by recall.}
\label{tab:prf-supplement}
\begin{tabular}{@{}lccc@{}}
\toprule
Model & Recall ($95\%$ CI) & Precision ($95\%$ CI) & F1 ($95\%$ CI)\\
\midrule
Gemini 3.1 Pro & $0.698$ ($0.630$-$0.765$) & $0.755$ ($0.685$-$0.825$) & $0.725$ ($0.658$-$0.790$)\\
DeepSeek V4 Pro & $0.645$ ($0.560$-$0.730$) & $0.705$ ($0.632$-$0.775$) & $0.674$ ($0.596$-$0.751$)\\
GPT 5.5 & $0.645$ ($0.600$-$0.692$) & $0.765$ ($0.710$-$0.815$) & $0.700$ ($0.654$-$0.744$)\\
Gemma 4 31B & $0.638$ ($0.578$-$0.698$) & $0.761$ ($0.681$-$0.838$) & $0.694$ ($0.630$-$0.756$)\\
GLM 5.2 & $0.607$ ($0.542$-$0.667$) & $0.662$ ($0.592$-$0.732$) & $0.633$ ($0.567$-$0.700$)\\
Kimi K2.6 & $0.604$ ($0.548$-$0.656$) & $0.723$ ($0.638$-$0.806$) & $0.658$ ($0.594$-$0.717$)\\
Qwen 3.7 Max & $0.582$ ($0.524$-$0.639$) & $0.649$ ($0.589$-$0.709$) & $0.614$ ($0.558$-$0.668$)\\
Claude Opus 4.8 & $0.578$ ($0.512$-$0.643$) & $0.660$ ($0.595$-$0.720$) & $0.616$ ($0.555$-$0.676$)\\
Grok 4.3 & $0.575$ ($0.522$-$0.625$) & $0.808$ ($0.765$-$0.855$) & $0.672$ ($0.634$-$0.708$)\\
Mistral Large 3 & $0.565$ ($0.485$-$0.640$) & $0.652$ ($0.568$-$0.720$) & $0.606$ ($0.524$-$0.674$)\\
GPT-OSS 120B & $0.541$ ($0.468$-$0.612$) & $0.596$ ($0.522$-$0.666$) & $0.567$ ($0.496$-$0.638$)\\
Llama 4 Maverick & $0.502$ ($0.432$-$0.580$) & $0.582$ ($0.495$-$0.675$) & $0.540$ ($0.464$-$0.617$)\\
Llama 3.3 70B & $0.458$ ($0.400$-$0.518$) & $0.528$ ($0.445$-$0.618$) & $0.490$ ($0.423$-$0.560$)\\
\bottomrule
\end{tabular}
\end{table*}

\subsection{Pairwise model comparisons}
\label{app:pairwise_results}

The $78$ pairwise model comparisons are supplementary and are not used to establish an inferential ranking in the main paper. The accompanying analysis files report mean recall differences, raw $p$-values, and Benjamini--Hochberg-adjusted $p$-values for the procedures in Appendix~\ref{app:model_pair_tests}. Fifteen comparisons survive adjustment when the $16$ topics are treated as separate sign-flip units, both with the original Monte Carlo calculation and with exhaustive enumeration. None survives when the eight matched pairs are retained as blocks; the smallest adjusted $p$-value is $0.087$. The mean differences are unchanged. This sensitivity concerns the inferential unit, not merely Monte Carlo sampling. Neither result establishes equivalence between models.

\subsection{Per-model WEIRD-Serbian comparisons}
\label{app:per_model_results}
\begin{table*}[t]
\centering
\small
\caption{Per-model WEIRD-minus-Serbian recall comparisons.
Positive gaps favour the WEIRD topic.
$p_{\mathrm{BH}}$ is adjusted across the $13$ generators.}
\label{tab:per_model_weird_gap}

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
\end{table*}

Table~\ref{tab:per_model_weird_gap} reports the per-model comparisons. No individual generator has a one-sided raw $p<0.05$, and none survives adjustment across the $13$ generators.
Figure~\ref{fig:paired-detail}, panel B, displays mean recall in each cultural group for every generator.

\section{Judge reliability and robustness}
\label{app:reliability}

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

\subsection{Pairwise judge agreement}
\label{app:pairwise_judges}

Pairwise Cohen's $\kappa$ is calculated for each pair of base-panel judges using only generated perspectives rated by both judges. The number of co-rated perspectives ranges from approximately $720$ to $880$ across judge pairs. Pairwise $\kappa$ values range from approximately $0.67$ to $0.85$. The three lowest values are $0.671$ for Gemini-Claude, $0.684$ for Gemini-GPT, and $0.695$ for Gemini-DeepSeek. These results show that judge decisions are related but not identical; they do not identify which judge is more accurate.

\subsection{Leave-one-judge-out robustness}
\label{app:lojo}

We repeat the aggregation after removing each of the seven models that appears anywhere in the judge roster. The remaining valid judgments are re-averaged before recall, precision, and F1 are recalculated.

Spearman correlations between the full-panel and leave-one-judge-out recall rankings range from $0.971$ to $0.999$. The corresponding F1-ranking correlations range from $0.978$ to $1.000$. Gemini 3.1 Pro remains first by F1 under every exclusion. The pooled WEIRD-minus-Serbian recall difference ranges from approximately $-0.008$ to $-0.020$, compared with $-0.013$ in the full analysis; the corresponding two-sided $p$-values range from approximately $0.38$ to $0.84$. The largest individual change in recall is $3.6$ percentage points for Llama 3.3 70B when the Gemini judge is removed.

\subsection{No-match decisions}
````

### With this

````latex
For overall recall, the US-minus-China difference is $-0.030$ ($95\%$ CI $[-0.048,-0.013]$), with raw $p=0.023$ and Holm-adjusted $p=0.047$. For the cultural gap, the difference is $-0.025$ ($95\%$ CI $[-0.082,0.025]$), with raw and adjusted $p=0.453$. These outcomes answer different questions: an overall recall difference does not establish a difference in the WEIRD-Serbian gap. The accompanying analysis files contain both contrasts and their uncertainty estimates.



\section{Judge reliability and robustness}
\label{app:reliability}

\subsection{Fleiss' kappa with incomplete panels}
\label{app:agreement_coefficients}
Each generated perspective is an item, with ratings mapped to its topic's canonical reference indices 1--5 or 0 for no match. We use the available four or five judgments per item. The variable-rater calculation averages within-item pairwise agreement, using the actual number of valid raters for each item, and estimates chance agreement from the pooled category frequencies across valid ratings. Fleiss' $\kappa$ is observed agreement minus expected agreement, divided by one minus expected agreement. Missing ratings are excluded rather than coded as no match. We calculate the coefficient overall and separately by cultural setting; it describes consistency, not accuracy.

\subsection{Leave-one-judge-out robustness}
\label{app:lojo}
We remove each of the seven models appearing in the judge roster in turn and repeat recall aggregation using the remaining valid judgments. The pooled WEIRD-minus-Serbian gap ranges from approximately $-0.020$ to $-0.008$, compared with $-0.013$ for the full panel. The largest individual-model change is an increase of $3.6$ percentage points for Llama 3.3 70B when Gemini is removed. These checks assess sensitivity to panel membership; additional ranking statistics are retained in the analysis files.

\subsection{No-match decisions}
````

## Swap 05 — Move alternative aggregation and crossed-model checks to the analysis files

**Original lines:** [858–875](/Users/vuk/Downloads/0_version_2.tex:858). **Revised lines:** [665–669](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:665).

### Replace this

````latex
All eight differences are non-zero, and no two have the same absolute value, so there are no tied ranks. The primary exact Wilcoxon signed-rank test uses a one-sided alternative of a positive shift in WEIRD-minus-Serbian recall and gives $p=0.6797$. The observed mean difference is $-0.0131$, and the median is $-0.0140$. For completeness, the two-sided result is $p=0.7422$, and the matched-pairs rank-biserial correlation is $-0.1667$. The signed-rank inference assumes independent pair-level differences and symmetry under the null; it does not directly test the arithmetic mean.

\subsection{Sensitivity analyses of the model-pair gaps}
\label{app:gap-sensitivity}
The primary test averages over generators within each matched pair. We also examine an alternative aggregation. The mean over eight pairs within each generator, $\overline d_m=\frac18\sum_p d_{mp}$. An exact signed-rank calculation uses these $13$ model means, removes numerical roundoff before ranking, assigns average ranks to ties, and enumerates every sign assignment. It gives one-sided $p=0.843$ and two-sided $p=0.331$. This comparison is conditional on the same eight pairs; the selected model families are not independent cultural replications.

To examine both dimensions, a crossed bootstrap independently resamples generator rows and matched-pair columns with replacement. Each of $10{,}000$ replicates retains the Cartesian-product submatrix. The resulting approximate $95$\% interval for the mean gap is $[-0.090,0.070]$. The resampling scheme follows \citet{owenPigeonholeBootstrap2007}.

A model-based check fits the $104$ model-pair differences using crossed random intercepts:
\begin{equation}
d_{mp}=\mu+u_m+v_p+\epsilon_{mp}.
\label{eq:crossed}
\end{equation}
Generator and pair effects and the residual are assumed independent. Restricted maximum likelihood gives $\mu=-0.013$ (SE $0.038$; $95$\% Wald CI $[-0.088,0.062]$; approximate two-sided $p=0.733$). The fit converged but produced a boundary warning, so the result remains a sensitivity check.

These procedures account for the two grouping dimensions under their respective assumptions. They do not establish that the selected models or topics are representative, or explicitly model dependence between different generators from the same developer family. The $104$ differences are not treated as independent replicates. The per-reference model in Appendix~\ref{app:mixed_model} is a separate specification.

\subsection{Exploratory category comparisons}
````

### With this

````latex
All eight differences are non-zero, and no two have the same absolute value, so there are no tied ranks. The primary exact Wilcoxon signed-rank test uses a one-sided alternative of a positive shift in WEIRD-minus-Serbian recall and gives $p=0.6797$. The observed mean difference is $-0.0131$, and the median is $-0.0140$. For completeness, the two-sided result is $p=0.7422$, and the matched-pairs rank-biserial correlation is $-0.1667$. The signed-rank inference assumes independent pair-level differences and symmetry under the null; it does not directly test the arithmetic mean.



\subsection{Exploratory category comparisons}
````

## Swap 06 — Move additional intervals and the power calculation to the analysis files

**Original lines:** [823–834](/Users/vuk/Downloads/0_version_2.tex:823). **Revised lines:** [637–641](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:637).

### Replace this

````latex
The mean is $-0.0131$, the SD is $0.107$, and the SE is $0.038$. The resulting interval is $[-0.103,0.077]$, or $-10.3$ to $7.7$ percentage points. The calculation assumes independent, approximately normally distributed pair-level differences. It estimates the arithmetic mean and is separate from the signed-rank test in Appendix~\ref{app:primary_wilcoxon}.

\paragraph{Supplementary interval and upper bound.}
The original percentile bootstrap resamples the eight matched pairs $10{,}000$ times, keeping all $13$ models together within each sampled pair. It uses seed $42$ and the saved random-number stream, giving $[-0.08096,0.05823]$. With only eight resampling units, percentile intervals may have limited coverage accuracy. The corresponding one-sided $95\%$ $t$ upper bound is $0.059$. This is conditional on the interval assumptions and the selected benchmark, not a general upper bound on cultural disparities.

\paragraph{Individual-model intervals.}
Table~\ref{tab:prf-supplement} retains the original $95\%$ percentile intervals for model-level recall, precision, and F1, based on $10{,}000$ resamples of the $16$ individual topics. These intervals do not retain matched-pair blocks. A sensitivity analysis for model recall instead resamples the eight matched pairs, retaining both topics and their equal weights, with $10{,}000$ resamples and a fresh NumPy generator using seed $42$. Both sets of recall intervals are supplied in the accompanying analysis files. The model means are unchanged. Neither overlapping intervals nor an absence of significant pairwise differences establishes model equivalence.

\paragraph{Illustrative sensitivity calculation.}
For a one-sided one-sample $t$-test at $\alpha=0.05$, normally distributed independent pair-level differences, and the observed between-pair SD, a hypothetical five-percentage-point WEIRD advantage gives approximately $32\%$ power. An advantage of about $10.5$ points gives $80\%$ power. These values use a noncentral $t$ distribution with seven degrees of freedom. They describe hypothetical effects under a $t$-test, not power at the observed effect or power of the exact Wilcoxon test.

\subsection{Primary WEIRD-Serbian signed-rank test}
````

### With this

````latex
The mean is $-0.0131$, the SD is $0.107$, and the SE is $0.038$. The resulting interval is $[-0.103,0.077]$, or $-10.3$ to $7.7$ percentage points. The calculation assumes independent, approximately normally distributed pair-level differences. It estimates the arithmetic mean and is separate from the signed-rank test in Appendix~\ref{app:primary_wilcoxon}.

Additional interval estimates, individual-model intervals, and the illustrative power calculation are retained in the accompanying analysis files.

\subsection{Primary WEIRD-Serbian signed-rank test}
````

## Swap 07 — Merge missing-data details and move precision/F1 definitions

**Original lines:** [777–817](/Users/vuk/Downloads/0_version_2.tex:777). **Revised lines:** [617–631](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:617).

### Replace this

````latex
With complete panels, these equations reduce to the mean judge recall in Eq.~\ref{eq:mean-judge-recall}. When judgments are missing, $|J_k|$ can differ across outputs; the cap prevents any reference receiving more than full credit. All outputs in this dataset have at least four valid judgments.

\subsection{Precision}
\label{app:precision_aggregation}

For generated perspective $k$, let $m_{jk}=1$ if judge $j$ assigns it to any reference perspective and $m_{jk}=0$ if the judge returns no match. Its precision contribution is

\begin{equation}
 q_k=\frac{1}{|J_k|}\sum_{j\in J_k}m_{jk}.
\end{equation}

Model-topic precision is

\begin{equation}
 P=\frac{1}{5}\sum_{k=1}^{5}q_k.
\end{equation}

Model-level recall and precision are the corresponding averages across the $16$ topics. Model-level F1 is the harmonic mean of model-level precision and recall.

A failed judge call is missing data and is excluded from the denominator. It is not treated as a no-match decision.

\subsection{Missing judgments and the recall cap}
\label{app:missing_judgments}

With a complete and identical judge panel across the five generations, the summed panel credit for a reference cannot exceed one. Missing judge calls can change the denominator from one generation to another, however. In that case, summing generation-level weights can produce a value slightly above one.

The implementation therefore caps each reference credit at one before topic recall is computed. The cap affects two observed credits for Grok 4.3 on the WEIRD topic in pair $8$: their uncapped values are $1.0167$ and $1.0917$. Both are set to $1$ in the published scores.

\subsection{Judgment execution and retries}
\label{app:judgment_counts}

The design requires $1{,}040\times5=5{,}200$ judge decisions. The raw judgment log contains $5,228$ records because failed calls that were retried remain in the log. Of these records, $44$ are failed or null calls. Twenty-eight were followed by successful retry records, leaving $16$ intended judgments unrecovered.

The final evaluation therefore contains $5,184$ valid decisions. Of the $1,040$ generated perspectives, $1,024$ have five valid judge decisions and $16$ have four. A no-match decision is a valid judgment in which the judge selects no reference. A missing judgment is an execution failure. The two are kept separate throughout the analysis.

\section{Statistical details}
\label{app:statistics}

\subsection{Confidence intervals and sensitivity calculations}
\label{app:bootstrap}

````

### With this

````latex
With complete panels, these equations reduce to the mean judge recall in Eq.~\ref{eq:mean-judge-recall}. When judgments are missing, $|J_k|$ can differ across outputs; the cap prevents any reference receiving more than full credit. All outputs in this dataset have at least four valid judgments.

\subsection{Missing judgments, the recall cap, and retries}
\label{app:missing_judgments}
\label{app:judgment_counts}
Missing calls are excluded from the valid-judge denominator; valid no-match decisions remain and earn zero credit. With complete panels, summed credit for each reference cannot exceed one. Different valid-judge denominators across outputs can otherwise produce larger totals, so Eq.~\ref{eq:topic-recall} caps each reference at one. The cap affects two credits for Grok 4.3 on the WEIRD topic in pair~8: $1.0167$ and $1.0917$, both set to $1$.

The design requires $5{,}200$ decisions. The raw log contains $5{,}228$ records, including $44$ failed or null calls; $28$ were followed by successful retries, leaving $16$ judgments unrecovered. The final $5{,}184$ valid decisions cover $1{,}024$ outputs with five judgments and $16$ with four. Supplementary precision and F1 definitions and results are retained in the accompanying analysis files.

\section{Statistical details}
\label{app:statistics}

\subsection{Confidence interval for the mean cultural gap}
\label{app:bootstrap}

````

## Swap 08 — Preserve developer-family definitions in Appendix C

**Original lines:** [724–727](/Users/vuk/Downloads/0_version_2.tex:724). **Revised lines:** [563–567](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:563).

### Replace this

````latex
\subsection{Family-disjoint judge panels}
\label{app:judge_panels}

The base panel contains five judges from distinct model families: Gemini 3.1 Pro, GPT 5.5, Claude Sonnet 5, DeepSeek V4 Pro, and Kimi K2.6. No generator is evaluated by a judge from the same model family. If a generator shares a family with a base-panel judge, that judge is replaced by a designated substitute. Generators from families not represented in the base panel use the unchanged five-judge panel. Table~\ref{tab:judge_substitutions} lists the substitutions.
````

### With this

````latex
\subsection{Family-disjoint judge panels}
\label{app:judge_panels}
Google includes Gemini and Gemma, OpenAI includes GPT and GPT-OSS, and Anthropic includes Claude Opus and Claude Sonnet.

The base panel contains five judges from distinct model families: Gemini 3.1 Pro, GPT 5.5, Claude Sonnet 5, DeepSeek V4 Pro, and Kimi K2.6. No generator is evaluated by a judge from the same model family. If a generator shares a family with a base-panel judge, that judge is replaced by a designated substitute. Generators from families not represented in the base panel use the unchanged five-judge panel. Table~\ref{tab:judge_substitutions} lists the substitutions.
````

## Swap 09 — Describe the accompanying analysis archive

**Original lines:** [599–603](/Users/vuk/Downloads/0_version_2.tex:599). **Revised lines:** [438–442](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:438).

### Replace this

````latex

\section{Data and code availability}
 The final repository or archival identifier will be added before submission.

\section{Acknowledgments}
````

### With this

````latex

\section{Data and code availability}
The accompanying analysis files preserve the supplementary analyses omitted from this shorter article, including the sensitivity of individual-model comparisons to the unit of analysis. The final repository or archival identifier will be added before submission.

\section{Acknowledgments}
````

## Swap 10 — Replace alpha results with kappa; condense discussion and limitations

**Original lines:** [512–595](/Users/vuk/Downloads/0_version_2.tex:512). **Revised lines:** [400–434](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:400).

### Replace this

````latex
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

\section{Discussion}
\label{sec:Discussion}
The primary comparison found no detectable WEIRD recall advantage in this benchmark. Large differences between individual topic pairs occurred in both directions, while coverage remained incomplete in both cultural settings. The results therefore motivate attention to topic selection and to the particular perspectives that models omit.

\subsection{Interpreting the cultural comparison}
Research on pluralistic and culturally adaptive alignment motivated our expectation of better coverage in WEIRD contexts \citep{sorensenRoadmapPluralisticAlignment2024,fengModularPluralismPluralistic2024,wangMultilingualPromptingImproving2025}. This benchmark does not support it for the selected controversies.

The primary matched-pair comparison provides no evidence for the predicted WEIRD recall advantage. Judge agreement was also similar across the two settings, although this does not establish equal error rates. These findings concern the selected controversies under direct elicitation in English. They do not establish equal representation across cultures, languages, or tasks.

Several explanations remain possible. Contemporary training data may contain enough regional and multilingual material to recover well-documented Serbian positions when models are explicitly asked for diverse perspectives. Retrieval limitations or post-training behaviour may constrain coverage across controversies more generally. The five-perspective output limit also creates competition among legitimate positions for inclusion. The experiment does not distinguish these explanations.

Topic selection matters when interpreting the result. Variation across controversies was much larger than the pooled cultural difference, with large pair differences favouring both settings. An unmatched comparison could misattribute such variation to cultural setting. Structural matching reduces this ambiguity, although it cannot remove all differences between controversies.

\subsection{Incomplete coverage remains}
\label{sec:Incomplete coverage remains the main problem}
The absence of a detectable WEIRD advantage does not imply comprehensive coverage. Even the strongest models omit a substantial share of the reference perspectives. In this benchmark, omissions occur across both cultural settings rather than consistently concentrating in one.

Recall varies within each access and size category, and individual scores overlap across categories. Although the observed category means differ, none of the four exploratory comparisons reaches the adjusted significance threshold. These results do not establish equivalence between categories or identify the effects of size and openness separately.

Future work could examine what makes particular controversies or perspectives difficult to recover. Candidate factors include the amount and visibility of documentation, the prominence of positions in training data, and their responsiveness to elicitation after post-training. Measuring these properties directly would allow them to be tested as predictors, rather than inferred from cultural or model-level averages.

\subsection{Implications for evaluation and culturally adaptive systems}
\label{sec:Implications for evaluation and culturally adaptive systems}
The matched design can support comparisons involving other populations. Its purpose is to make differences in perspective coverage easier to interpret by accounting for topic selection. Coverage should also be evaluated directly. General capability, multilingual performance, and overall answer quality do not establish that a model will recover the positions relevant to a contested issue.

The appropriate intervention depends on the observed deficit. A systematic cultural coverage gap may motivate targeted cultural or linguistic adaptation. If coverage is incomplete across both sides of a matched comparison, improving the retrieval or elicitation of omitted perspectives may be more relevant. The present result does not make cultural adaptation unnecessary; instead it helps specify what an intervention would need to address.

This distinction also matters for AI-mediated deliberation. Systems that expose disagreement, support consensus, or introduce minority positions depend on the perspectives available to them \cite{tesslerAICanHelp2024a, chiangEnhancingAIAssistedGroup2024b, leeAmplifyingMinorityVoices2025a}. A perspective that never enters the candidate set cannot inform those later processes. Perspective recall is thus a prerequisite for their use of diverse positions, not a substitute for deliberation itself.

\section{Limitations}
\label{sec:Limitations}
The findings apply to a finite reference benchmark, a selected set of models and topics, and one elicitation and judging procedure.

\subsection{The reference sets are not exhaustive}
\label{sec:The reference sets are not exhaustive}
Each topic has five externally documented reference perspectives that a single author constructed. Reference statements for Serbian topics are English summaries of sources in more than one language, so summarisation and translation choices may affect how closely model outputs match them. This common target supports comparison across topics, but it cannot represent every legitimate position within a population. Recall therefore measures coverage of the reference set. Similarly, an output that matches no reference receives no precision credit even if it expresses a legitimate position outside the benchmark. Absolute recall and precision values should be read in this context. Their main value here is comparison under a common construction procedure.

\subsection{Judge agreement does not establish judge validity}
\label{sec:Judge agreement does not establish judge validity}
The scores depend on LLM judgments of whether generated and reference perspectives express the same stance. Agreement and judge-removal checks describe consistency and sensitivity to panel membership. They do not establish correctness, because judges may share errors. Excluding judges from the generator's developer family prevents direct within-family evaluation but does not remove shared biases or differences in judge strictness.

\subsection{Eight matched pairs limit statistical resolution}
\label{sec:Eight matched pairs limit the size of effects we can resolve}
The primary comparison rests on eight topic pairs whose recall differences vary widely (SD $10.7$ percentage points). The $95\%$ confidence interval for the mean gap spans $-10.3$ to $7.7$ points, leaving differences in either direction compatible with the data under the interval's assumptions. Eight investigator-selected pairs provide limited statistical resolution and do not represent a random sample of cultural controversies. We therefore report no detectable WEIRD advantage, not equivalent coverage. Alternative intervals and an illustrative sensitivity calculation appear in Appendix~\ref{app:bootstrap}.

\subsection{Serbia is one non-WEIRD setting}
\label{sec:Serbia is one non-WEIRD case}
The Serbian controversies studied here are European, relatively well documented, and often discussed in multilingual or internationally indexed sources. They represent one non-WEIRD setting. The findings cannot be generalised to all non-WEIRD populations. Larger coverage gaps may occur in less documented societies, lower-resource languages, or political contexts with less international attention. Matched comparisons involving additional populations are needed to test this possibility.

\subsection{The paper tests direct elicitation at one point in time}
\label{sec:The paper tests direct elicitation in a single model snapshot}
We explicitly asked models for diverse perspectives. The benchmark therefore measures recovery under direct elicitation, rather than the perspectives models would spontaneously include in ordinary conversation. All prompts were in English, holding elicitation and judging language constant across settings. The study does not test Serbian-language or multilingual prompting, which may produce different coverage patterns.

The results also reflect one snapshot of changing model systems. Rankings may change as those systems are updated. The matched design is intended to remain useful beyond the evaluated model versions.

\subsection{Structural matching reduces but does not eliminate topic confounding}
\label{sec:Structural matching reduces but does not eliminate topic confounding}
The pairs share broad political structures, but may differ in documentation, historical depth, polarisation, and training-data prevalence. Matching improves the interpretability of the comparison without experimentally isolating cultural setting. It was investigator-guided rather than based on a prespecified quantitative rule, and alternative pairings may be defensible.

Releasing the topic definitions, matching rationales, reference perspectives, and their supporting sources will allow others to inspect these choices and test alternative pairings.

\section{Conclusion}
````

### With this

````latex
\subsection{Descriptive checks on judge consistency}
\label{sec:judge-checks}
Fleiss' $\kappa$ is $0.768$ overall, $0.761$ for WEIRD topics, and $0.774$ for Serbian topics. Judge-level no-match rates are $32.9\%$ and $31.1\%$ in the two settings. Removing one judge at a time changes the pooled WEIRD-minus-Serbian recall gap from $-1.3$ percentage points to between approximately $-2.0$ and $-0.8$ points (Appendix~\ref{app:lojo}). The observed gap remains small and negative under each removal; neither similar agreement nor this stability establishes equal judge error rates.

\section{Discussion}
\label{sec:Discussion}
\subsection{Interpreting the cultural comparison}
Research on pluralistic and culturally adaptive alignment motivated our expectation of better coverage in WEIRD contexts \citep{sorensenRoadmapPluralisticAlignment2024,fengModularPluralismPluralistic2024,wangMultilingualPromptingImproving2025}. The matched comparison does not support this expectation for the selected controversies. Pair-level differences run in both directions and are much larger than the pooled difference, making topic selection central to interpretation.

Contemporary training data may contain enough regional and multilingual material to recover well-documented Serbian positions under direct elicitation. Retrieval limitations, post-training behaviour, or competition within the five-perspective output budget may also constrain coverage across settings. The experiment does not distinguish these explanations. Future work could measure documentation, prominence in training data, and responsiveness to elicitation as predictors of omitted perspectives.

\subsection{Incomplete coverage and implications for evaluation}
\label{sec:Incomplete coverage remains the main problem}
\label{sec:Implications for evaluation and culturally adaptive systems}
The absence of a detectable WEIRD advantage does not imply comprehensive coverage: even the highest-recall model misses approximately $30\%$ of the reference coverage. Variation within model categories and the inconclusive category comparisons also caution against treating access or relative size as a substitute for direct coverage measurement.

Matched evaluations can extend to other populations and help specify the deficit an intervention should address. A systematic cultural gap may motivate targeted cultural or linguistic adaptation; omissions across both sides of a comparison may instead motivate better retrieval or elicitation. The present result does not make cultural adaptation unnecessary.

AI-mediated deliberation systems that expose disagreement, support consensus, or introduce minority positions depend on the perspectives available to them \cite{tesslerAICanHelp2024a,chiangEnhancingAIAssistedGroup2024b,leeAmplifyingMinorityVoices2025a}. Positions omitted from the candidate set cannot inform those processes. Perspective recall is therefore a prerequisite for using diverse positions, not a substitute for deliberation.

\section{Limitations}
\label{sec:Limitations}
\paragraph{Reference construction and scope.}
Each topic has five externally documented references constructed by one author. They provide a common comparison target, not an exhaustive account of legitimate positions. English summaries of sources in more than one language may introduce summarisation or translation choices that affect matching. An unmatched output may express a legitimate position outside the reference set.

\paragraph{Judge validity.}
Agreement and judge-removal checks do not establish correctness: judges may share errors. Excluding judges from the generator's developer family prevents direct within-family evaluation but does not remove shared biases, culturally differential errors, or differences in strictness between panels.

\paragraph{Statistical resolution and topic selection.}
The eight investigator-selected pairs are not a random sample of controversies. Their gaps vary widely (SD $10.7$ percentage points), and the primary $95\%$ interval spans $-10.3$ to $7.7$ points. We therefore report no detectable WEIRD advantage, not equivalent coverage. Structural matching reduces topic confounding without isolating cultural setting: pairs may differ in documentation, historical depth, polarisation, and training-data prevalence. Matching used investigator judgment rather than a prespecified quantitative rule, and alternative pairings may be defensible. Releasing the references, sources, and matching rationales supports inspection and replication.

\paragraph{Population, prompting, and time.}
Serbia is one European, relatively well-documented non-WEIRD setting whose controversies often appear in multilingual or internationally indexed sources. Findings cannot be generalised to all non-WEIRD populations; less documented settings may have larger gaps. We tested direct requests for diverse perspectives in English, not spontaneous coverage or Serbian-language and multilingual prompting. Results reflect one model snapshot and one retained response per model-topic cell, without estimating repeated-generation variability; rankings may change as systems are updated.

\section{Conclusion}
````

## Swap 11 — Retain the model-comparison qualification and update the table caption

**Original lines:** [449–458](/Users/vuk/Downloads/0_version_2.tex:449). **Revised lines:** [337–346](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:337).

### Replace this

````latex
\subsection{RQ2: Recall by model and access category}
\label{sec:rq2}
Table~\ref{tab:model-recall} reports overall recall and separate means for WEIRD and Serbian topics. Overall recall ranges from $0.458$ for Llama 3.3 70B to $0.698$ for Gemini 3.1 Pro. Even the highest-recall model leaves approximately $30\%$ of the reference coverage unrecovered on average. These are descriptive comparisons of the selected models; the ordering does not establish that every difference between models is statistically distinguishable. Model-level intervals and pairwise tests appear in Appendices~\ref{app:prf-results}, \ref{app:bootstrap}, and~\ref{app:pairwise_results}.

\begin{table*}[!t]
\centering
\small
\caption{Perspective recall by model category. Each topic receives equal weight. Models are ordered by overall recall within each category. Supplementary intervals are reported in Appendix~\ref{app:prf-results}, with the matched-pair sensitivity analysis described in Appendix~\ref{app:bootstrap}.}
\label{tab:model-recall}
\begin{tabular}{lccc}
````

### With this

````latex
\subsection{RQ2: Recall by model and access category}
\label{sec:rq2}
Table~\ref{tab:model-recall} reports overall recall and separate means for WEIRD and Serbian topics. Overall recall ranges from $0.458$ for Llama 3.3 70B to $0.698$ for Gemini 3.1 Pro. Even the highest-recall model leaves approximately $30\%$ of the reference coverage unrecovered on average. These are descriptive comparisons. Supplementary individual-model significance findings change when matched topic pairs are preserved rather than treating topics separately; we therefore do not claim an inferential ranking. The accompanying analysis files retain both procedures and their results.

\begin{table*}[!t]
\centering
\small
\caption{Perspective recall by model category. Each topic receives equal weight. Models are ordered by overall recall within each category. Individual-model comparisons are descriptive.}
\label{tab:model-recall}
\begin{tabular}{lccc}
````

## Swap 12 — Update the RQ1 pointers to supplementary material

**Original lines:** [438–442](/Users/vuk/Downloads/0_version_2.tex:438). **Revised lines:** [326–330](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:326).

### Replace this

````latex
Four matched pairs favour WEIRD topics and four favour Serbian topics. The largest differences point in opposite directions: recall is $19.1$ percentage points higher for German immigration than for its Serbian migration-route counterpart, but $16.9$ points lower for Canadian residential schools than for Srebrenica. Mean topic recall ranges from $0.449$ for the Serbian migration-route topic to $0.685$ for Serbia's West-versus-Russia alignment. Both extremes occur among the Serbian topics, indicating that topic-level variation does not follow a uniform cultural direction.

Figure~\ref{fig:paired-recall} shows all eight pair-level differences. Additional analyses and alternative uncertainty estimates are reported in Appendix~\ref{app:statistics}; they do not change the interpretation of the primary comparison. Appendix~\ref{app:paired-views} presents the model-level and individual model-pair views.

\begin{figure*}[!t]
````

### With this

````latex
Four matched pairs favour WEIRD topics and four favour Serbian topics. The largest differences point in opposite directions: recall is $19.1$ percentage points higher for German immigration than for its Serbian migration-route counterpart, but $16.9$ points lower for Canadian residential schools than for Srebrenica. Mean topic recall ranges from $0.449$ for the Serbian migration-route topic to $0.685$ for Serbia's West-versus-Russia alignment. Both extremes occur among the Serbian topics, indicating that topic-level variation does not follow a uniform cultural direction.

Figure~\ref{fig:paired-recall} shows all eight pair-level differences. Appendix~\ref{app:statistics} gives the primary calculations; additional sensitivity analyses are retained in the accompanying analysis files.

\begin{figure*}[!t]
````

## Swap 13 — Use Fleiss’ kappa in the statistical methods

**Original lines:** [429–433](/Users/vuk/Downloads/0_version_2.tex:429). **Revised lines:** [317–321](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:317).

### Replace this

````latex

\paragraph{Check judge consistency.}
We report nominal Krippendorff's $\alpha$ overall and separately for WEIRD and Serbian topics, together with judge-level no-match rates. We also recalculate scores after removing each judge in turn. These checks assess agreement and sensitivity to panel membership; they do not establish that the judgments are correct. Additional agreement measures and detailed results appear in Appendix~\ref{app:reliability}.

\section{Results}
````

### With this

````latex

\paragraph{Check judge consistency.}
We report Fleiss' $\kappa$ overall and separately for WEIRD and Serbian topics, using a variable-rater formulation that excludes missing judgments (Appendix~\ref{app:agreement_coefficients}). We also report judge-level no-match rates and recalculate recall after removing each judge in turn. These checks assess consistency and sensitivity to panel membership, not correctness.

\section{Results}
````

## Swap 14 — Make individual-model comparisons descriptive

**Original lines:** [421–425](/Users/vuk/Downloads/0_version_2.tex:421). **Revised lines:** [309–313](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:309).

### Replace this

````latex

\paragraph{RQ2: describe models and compare categories.}
We report overall, WEIRD, and Serbian recall for each model. For category comparisons, we first average the two topics within each matched pair and then average across models within each category, giving models equal weight. We compare the three categories pairwise and compare Frontier with all eight open-weight models combined. Individual-model intervals and pairwise tests are supplementary.

\paragraph{RQ3: compare developer groups.}
````

### With this

````latex

\paragraph{RQ2: describe models and compare categories.}
We report overall, WEIRD, and Serbian recall for each model. For category comparisons, we first average the two topics within each matched pair and then average across models within each category, giving models equal weight. We compare the three categories pairwise and compare Frontier with all eight open-weight models combined. Individual-model comparisons are descriptive; supplementary analyses are retained in the accompanying analysis files.

\paragraph{RQ3: compare developer groups.}
````

## Swap 15 — Shorten generation, judging, and recall; remove the duplicate model table

**Original lines:** [293–406](/Users/vuk/Downloads/0_version_2.tex:293). **Revised lines:** [260–294](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:260).

### Replace this

````latex
\subsubsection{Models and perspective generation}
\label{sec:perspective-generation}
We evaluate $13$ models (Table~\ref{tab:generators}) and retain one response for each model-topic combination. The prompt asks for five distinct perspectives genuinely held within the specified population. Each perspective is written in an advocate's voice. The prompt allows fewer than five positions if appropriate. All $208$ retained responses contain five, giving $1{,}040$ generated perspectives, and no model declined the task. Appendix~\ref{app:generator_prompt} reproduces the prompt.

All generator prompts, judge prompts, and reference statements are in English. This holds elicitation and judging language constant across the two settings. Generators and judges were queried through the OpenRouter API with temperature zero, a fixed request seed, and a requested limit of $4{,}096$ completion tokens. The seed takes effect only for providers that support seeded sampling. We set no reasoning parameters and did not pin providers, so each model used OpenRouter's default reasoning behaviour and provider routing. The serving provider was not recorded. A response that could not be parsed received one repair request, and calls that still failed were re-run later. Valid responses were saved immediately and never regenerated, so no valid response was discarded. Each model-topic cell therefore has a single sample, and the analysis does not capture variation across repeated generations. Generation records date from 9-10 July 2026; judging, including retries, spans 10-20 July 2026. Appendix~\ref{app:execution} lists the configured model identifiers.

For the exploratory category comparison, we group the models into five Frontier systems, six larger open-weight systems, and two smaller open-weight systems. Frontier denotes systems without a verified public-weight release; Qwen 3.7 Max is included because Alibaba documents it as a commercial API model.\footnote{See \href{https://www.alibabacloud.com/en/news/product/maxcompute-model-computing-service-supports-qwen37-max-and-other-commercial-models-mkv}{Alibaba Cloud's Qwen3.7-Max commercial-model announcement}.} The smaller open-weight group consists of the two selected systems labelled 31B and 70B, Gemma 4 31B and Llama 3.3 70B. The other six open-weight systems form the larger group. These labels identify the groups used in this comparison rather than a general size taxonomy. The categories describe access and relative size, not capability. All $13$ systems were queried through the same API workflow. Appendix~\ref{app:execution} records category membership and release-source links.

\begin{table}[t]
\centering\small
\caption{The $13$ generators, grouped by the access and relative-size categories used throughout the analysis.}
\label{tab:generators}
\begin{tabularx}{\columnwidth}{@{}Yl@{}}
\toprule
Model & Developer \\
\midrule
\multicolumn{2}{@{}l}{\textit{Frontier (5)}}\\
Claude Opus 4.8 & Anthropic\\
GPT 5.5 & OpenAI\\
Gemini 3.1 Pro & Google\\
Grok 4.3 & xAI\\
Qwen 3.7 Max & Alibaba\\
\addlinespace
\multicolumn{2}{@{}l}{\textit{Larger open-weight (6)}}\\
DeepSeek V4 Pro & DeepSeek\\
Kimi K2.6 & Moonshot\\
GLM 5.2 & Z.AI\\
Llama 4 Maverick & Meta\\
Mistral Large 3 & Mistral\\
GPT-OSS 120B & OpenAI\\
\addlinespace
\multicolumn{2}{@{}l}{\textit{Smaller open-weight (2)}}\\
Gemma 4 31B & Google\\
Llama 3.3 70B & Meta\\
\bottomrule
\end{tabularx}
\end{table}

\subsubsection{Judge assignments}
\label{sec:Judge evaluation}
All five LLM judges perform the same matching task independently. Each receives one generated perspective at a time, along with the topic, target population, and all five reference perspectives. The judge selects the single reference that expresses the same underlying side and stance, or returns no match. Each decision includes a brief justification. Thematic overlap alone is insufficient. Outputs voiced from outside the target population also receive no match, although no saved output was flagged for this reason. Each judge evaluates all five generated perspectives separately, giving five assignments per judge and $25$ intended assignments per model-topic response. Judges do not see one another’s decisions. We then use these assignments about individual perspectives to calculate recall for the model’s complete set of five outputs on that topic.

For example, all five judges matched a GPT 5.5 output supporting UK fracking for energy security, jobs, and reduced import dependence to reference 1 in Table~\ref{tab:reference-example}. A different output opposed fracking because it distrusted companies and regulators. Claude Sonnet~5 matched it to reference 2, whereas the other four judges returned no match. This disagreement concerns correspondence to the reference set, not whether the output expresses a legitimate position. Appendix~\ref{app:worked-example} shows the saved outputs and all assignments. Judges evaluated both summaries and explanations.

We use \emph{family-disjoint judging}: no judge shares the generator's configured developer family. Google includes Gemini and Gemma, OpenAI includes GPT and GPT-OSS, and Anthropic includes Claude Opus and Claude Sonnet. The five judges in each panel also come from different developer families.

The base panel contains Gemini 3.1 Pro, GPT 5.5, Claude Sonnet 5, DeepSeek V4 Pro, and Kimi K2.6. When a generator shares a family with one of these judges, we replace that judge with a designated substitute, keeping five seats. Grok 4.5 substitutes for Google, OpenAI, Anthropic, or Moonshot; Qwen 3.7 Max substitutes for DeepSeek. Appendix~\ref{app:judge_panels} gives the mapping. Each generator is judged by the same panel on its WEIRD and Serbian topics, avoiding changes in panel membership between the two settings. This does not exclude topic-dependent or culturally differential judging errors. Differences between panels may also affect comparisons of overall recall between generators (Section~\ref{sec:rq2}).

Reference order is randomised independently for every judgment, and returned indices are mapped back to the original identifiers. The design requires $25$ decisions per model-topic response, or $5{,}200$ in total. After retries, $5{,}184$ decisions are valid: $1{,}024$ outputs have five judgments and $16$ have four. Failed calls are missing data. A valid no-match decision remains in the calculation and earns zero credit (Appendix~\ref{app:judgment_counts}).

\subsubsection{From assignments to recall}
\label{sec:recall}
Recall measures the proportion of a topic’s five reference perspectives recovered by a model’s five generated perspectives. Repeated matches to the same reference do not increase coverage. We use the judges’ assignments for individual perspectives to calculate recall for each model on each topic. Averaging these scores across topics gives a model’s mean recall; averaging them across models gives a topic’s mean recall. The calculation proceeds in three steps.

\paragraph{Step 1: calculate coverage from one judge's assignments.}
For a given model and topic, we count the distinct references recovered
across one judge's five assignments. We divide this count by five,
the number of reference perspectives. In the worked example
(Tables~\ref{tab:reference-example} and~\ref{tab:fracking-matches}),
Claude Sonnet~5 assigns GPT~5.5's outputs to references
2, 2, 1, 5, and 1. These assignments recover references 1, 2, and 5,
giving GPT~5.5 a recall of $3/5=0.60$ on this topic according to
Claude's assignments. All five outputs match a reference, but they
cover only three of the five references. Precision counts matching
outputs; recall counts distinct references recovered.

\paragraph{Step 2: combine the judges for one model and topic.}
Let $m$ identify the model, $t$ the topic, and $j$ the judge. Write $R_{mtj}$ for recall calculated from judge $j$'s assignments. When all five judges supply valid decisions for all five outputs, model-topic recall is their mean:
\begin{equation}
R_{mt}=\frac{1}{5}\sum_{j=1}^{5}R_{mtj}.
\label{eq:mean-judge-recall}
\end{equation}

In this example, Gemini, Claude, DeepSeek, and Kimi each match the
outputs to three distinct references, while Grok matches them to two.
The corresponding recall values are 0.60, 0.60, 0.60, 0.60, and 0.40.
Averaging these gives $R_{mt}=[4(0.60)+0.40]/5=0.56$.
The same result follows from the reference credits: references 1 and 2
receive full credit, and references 3 and 4 receive zero. Reference 5
receives $4/5=0.80$ credit because four judges recover it.
Averaging these five reference credits also gives 0.56.
No majority-vote threshold is applied.

When judgments are missing, the available judges can differ between outputs. The calculation therefore splits duplicate matches within each judge, averages the resulting credits over valid judges for each output, and caps each reference's total credit at one. Appendix~\ref{app:recall_aggregation} gives the exact equations, which reduce to Eq.~\ref{eq:mean-judge-recall} for complete panels. Every output has at least four valid judgments. A missing judgment is excluded; a valid no-match decision remains and earns zero credit.

\paragraph{Step 3: summarise across topics or models.}
The evaluation gives one recall score $R_{mt}$ for each of the
$13\times16=208$ model-topic combinations. These scores form a
table with models as rows and topics as columns. Averaging a row
gives a model's mean recall across topics; averaging a column
gives a topic's mean recall across models.

For model $m$, we average recall across all $16$ topics,
giving each topic equal weight:
\begin{equation}
\overline R_m=\frac{1}{16}\sum_{t=1}^{16}R_{mt}
=\frac{\overline R_m^{\mathrm W}+\overline R_m^{\mathrm S}}{2}.
\label{eq:model-recall}
\end{equation}
Here, $\overline R_m^{\mathrm W}$ is the model's mean recall
across its eight WEIRD topics, and $\overline R_m^{\mathrm S}$
is its mean recall across its eight Serbian topics.

For topic $t$, we average recall across all $13$ models,
giving each model equal weight:
\[
\overline R_t=\frac{1}{13}\sum_{m=1}^{13}R_{mt}.
\]
We calculate both summaries from the model-topic scores without
any additional judge decisions. Precision and F1 are defined in
Appendix~\ref{app:precision_aggregation} and reported in
Appendix~\ref{app:prf-results}.

\subsubsection{Comparisons and statistical analysis}
````

### With this

````latex
\subsubsection{Models and perspective generation}
\label{sec:perspective-generation}
We evaluate the $13$ models in Table~\ref{tab:model-recall}, retaining one response per model-topic combination. The prompt requests five distinct perspectives held within the target population, written in an advocate's voice, but permits fewer if appropriate. All $208$ retained responses contain five perspectives, giving $1{,}040$ outputs; no model declined the task. Appendix~\ref{app:generator_prompt} reproduces the prompt.

All prompts and references are in English. Generators and judges were queried through OpenRouter with temperature zero, a fixed request seed where supported, and a requested limit of $4{,}096$ completion tokens. We set no reasoning parameters and did not pin or record serving providers. Malformed responses could receive one repair request and failed calls could be retried; valid responses were saved and never regenerated. Each model-topic cell has one sample, so repeated-generation variability is unmeasured. Appendix~\ref{app:execution} records identifiers and execution dates.

The exploratory categories contain five Frontier systems without verified public-weight releases, six larger open-weight systems, and two smaller open-weight systems (Gemma 4 31B and Llama 3.3 70B). Qwen 3.7 Max is classified as Frontier because Alibaba documents it as a commercial API model.\footnote{See \href{https://www.alibabacloud.com/en/news/product/maxcompute-model-computing-service-supports-qwen37-max-and-other-commercial-models-mkv}{Alibaba Cloud's Qwen3.7-Max commercial-model announcement}.} These categories describe access and relative size within this selection, not capability or a general size taxonomy. Developer mappings and release sources appear in Appendix~\ref{app:execution}.

\subsubsection{Judge assignments}
\label{sec:Judge evaluation}
Five LLM judges independently evaluate each generated perspective alongside the topic, target population, and all five reference perspectives. They receive summaries and explanations, select the reference expressing the same underlying side and stance or return no match, and briefly justify the decision. Thematic overlap alone is insufficient. Outputs voiced from outside the target population also receive no match, although none was flagged for this reason. Judges do not see one another's decisions. Appendix~\ref{app:judge_prompt} gives the prompt.

No judge shares the generator's configured developer family, and each panel's five judges come from different families. Designated substitutes maintain five seats; Appendix~\ref{app:judge_panels} gives the roster and family definitions. Each generator uses the same panel across WEIRD and Serbian topics. This controls panel membership within the cultural comparison, although different panels may affect comparisons between generators.

Reference order is randomised independently for every judgment, then returned indices are mapped back to the original identifiers. Of $5{,}200$ intended decisions, $5{,}184$ are valid after retries: $1{,}024$ outputs have five judgments and $16$ have four. Failed calls are missing data; a valid no-match decision remains in the calculation and earns zero credit.

\subsubsection{From assignments to recall}
\label{sec:recall}
Recall measures the proportion of a topic's five reference perspectives recovered by a model's five outputs. Repeated matches to one reference do not increase coverage.

\paragraph{Step 1: calculate coverage for one judge.}
Count the distinct references recovered across that judge's five assignments and divide by five. In the UK fracking example, Claude Sonnet~5 assigns GPT~5.5's outputs to references 2, 2, 1, 5, and 1. Three distinct references are recovered, giving recall $3/5=0.60$ (Appendix~\ref{app:worked-example}).

\paragraph{Step 2: combine the judges.}
For model $m$, topic $t$, and judge $j$, let $R_{mtj}$ denote judge-specific recall. With complete judgments, model-topic recall is
\begin{equation}
R_{mt}=\frac{1}{5}\sum_{j=1}^{5}R_{mtj}.
\label{eq:mean-judge-recall}
\end{equation}
Four judges in the example recover three references and one recovers two, giving $R_{mt}=[4(0.60)+0.40]/5=0.56$. No majority-vote threshold is applied. For incomplete panels, duplicate matches are split within each judge, credits are averaged over valid judges for each output, and each reference's total credit is capped at one. Appendix~\ref{app:recall_aggregation} gives the exact calculation, which reduces to Eq.~\ref{eq:mean-judge-recall} for complete panels.

\paragraph{Step 3: summarise the model-topic scores.}
The $13\times16=208$ scores form a model-by-topic table. Averaging across the $16$ topics gives a model's overall recall; averaging its eight topics in each setting gives WEIRD and Serbian recall. Averaging across the $13$ models gives a topic's mean recall. Topics and models receive equal weight in their respective summaries.

\subsubsection{Comparisons and statistical analysis}
````

## Swap 16 — Shorten reference construction and remove the main-text fracking table

**Original lines:** [262–289](/Users/vuk/Downloads/0_version_2.tex:262). **Revised lines:** [250–256](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:250).

### Replace this

````latex
\subsection{Constructing the reference sets}
\label{sec:referencesets}
A reference perspective is a substantively distinct stance documented as being held within the target population. The first author constructed all $80$ reference perspectives manually from research literature and news reporting, drawing on surveys, polling, referendum results, peer-reviewed research, and clearly attested public debate. The reference statements summarise positions supported by these sources, rather than positions generated by the models evaluated here. The first author selected five distinct stances per topic from the linked sources. The source workbook records a source entry for each of the $80$ perspectives. The accompanying source ledger links the evaluated reference identifiers to their workbook cells and preserves both the source text and any embedded hyperlink. All reference summaries and explanations in the workbook match the evaluated reference set exactly. Source entries identify the evidence used in construction.

Reference summaries and explanations were written in English. Sources cited for Serbian topics include English-language research, reporting, and survey materials. The language of the cited material was therefore not uniformly Serbian.

Each topic has five references so that all topics share the same evaluation budget. This is a design choice, not a claim that a controversy has exactly five legitimate positions. The score measures recovery of these references; it does not measure every position that might exist outside them. Each stored perspective consists of a short summary and a longer explanation. Judges receive both.

Table~\ref{tab:reference-example} shows an actual reference set. It illustrates why identifying a broad side of a controversy is insufficient. Support for fracking may be unconditional, conditional, or opposed to local development; opposition may emphasise different grounds.

\begin{table}[t]
\centering\small
\caption{Reference summaries for UK fracking, reproduced from the benchmark. The target population is ``people in the United Kingdom''. Each record also contains an explanation.}
\label{tab:reference-example}
\begin{tabularx}{\columnwidth}{@{}rY@{}}
\toprule
ID & Reference summary \\
\midrule
1 & Restart UK fracking for energy security and jobs. \\
2 & Ban fracking permanently on environmental and seismic grounds. \\
3 & Support fracking in principle but oppose it locally. \\
4 & Reject fracking categorically on climate-emergency grounds. \\
5 & Conditional pragmatist, support shale gas only with strict guarantees and a transition plan. \\
\bottomrule
\end{tabularx}
\end{table}

\subsection{Evaluation procedure}
````

### With this

````latex
\subsection{Constructing the reference sets}
\label{sec:referencesets}
A reference perspective is a distinct stance documented as being held within the target population. The first author manually constructed all $80$ references from surveys, polling, referendum results, peer-reviewed research, and clearly attested public debate reported in research and news sources. The source workbook records the evidence for each perspective; the accompanying ledger links evaluated identifiers to workbook cells, source text, and embedded hyperlinks. The workbook's summaries and explanations match the evaluated reference set exactly.

All reference summaries and explanations were written in English. Sources for Serbian topics include English-language research, reporting, and surveys; the cited material was not uniformly Serbian. Five references per topic provide a common evaluation budget, without implying that a controversy has only five legitimate positions. Judges receive both the summary and explanation. The UK fracking example in Appendix~\ref{app:worked-example} illustrates distinctions between unconditional support, conditional support, local opposition, and different grounds for opposition.

\subsection{Evaluation procedure}
````

## Swap 17 — Condense related work

**Original lines:** [202–228](/Users/vuk/Downloads/0_version_2.tex:202). **Revised lines:** [202–216](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:202).

### Replace this

````latex
\section{Related work}
\label{sec:Related work}
Our paper connects research on cultural representation, perspective coverage, and LLM-based evaluation.

\subsection{Pluralistic alignment and cultural representation}
\label{sec:Pluralistic alignment and cultural representation}
Pluralistic alignment treats differences in human values and viewpoints as something to preserve, rather than collapse into a single preference target \cite{sorensenRoadmapPluralisticAlignment2024, fengModularPluralismPluralistic2024, aliOperationalizingPluralisticValues2025}. This matters for political questions, where a useful answer may need to represent conflicting positions.

\citet{sorensenRoadmapPluralisticAlignment2024} distinguish three forms of pluralism. Overton pluralism concerns the range of positions a model represents. Steerable pluralism concerns its ability to adopt a requested position. Distributional pluralism concerns whether output frequencies reflect a target population. Our benchmark measures Overton-style coverage: whether documented perspectives are recovered at all.

The concentration of training, preference, and evaluation data in WEIRD and English-language settings raises concerns about uneven cultural representation \cite{sorensenRoadmapPluralisticAlignment2024, wangMultilingualPromptingImproving2025, zewailMoralStereotypingLarge2026}. Multilingual and culturally adaptive prompting can improve diversity in some settings \cite{wangMultilingualPromptingImproving2025}. Language-specific evaluation resources also remain unevenly developed. Serbian SuperGLUE addresses gaps in complex language-understanding evaluation for Serbian and motivates broader coverage of South Slavic languages \cite{perovicSerbianSuperGLUEEvaluation2026}. This work motivates our directional hypothesis, but does not determine whether a particular coverage difference reflects cultural setting or the topics chosen for comparison.

\subsection{Measuring perspective coverage}
\label{sec:Measuring perspective coverage}
Political controversies rarely have a complete, uncontested set of correct labels. Perspectivist NLP therefore treats disagreement as part of the phenomenon being studied \cite{basileWeNeedConsider2021, plankProblemHumanLabel2022a, frendaPerspectivistApproachesNatural2025a}. Related approaches retain annotator-specific rationales or label distributions rather than combining all judgments into one target \cite{sarumiFineGrainedPerspectivesModeling2026, shettyLearningWhoDisagrees2026}. A fixed reference set can document positions known to exist, but cannot guarantee an exhaustive account of a debate.

Other work uses LLMs as proxies for human opinion. Under some prompting strategies, models can reproduce population-level polling patterns \cite{sunRandomSiliconSampling2024, gongCharacterizingAbilityLLMs2026}. Their apparent political or cultural preferences can also change with prompt design and methodology \cite{khanRandomnessNotRepresentation2025}. Hybrid approaches combine model-generated annotations with human attention to uncertain cases \cite{mehrotraMultiPerspectiveLLMAnnotations2026}. Our evaluation instead uses externally documented reference perspectives, keeping the scoring target separate from the models being evaluated.

The closest benchmark is OvertonBench, which evaluates perspective coverage using viewpoint groups derived from human responses and ratings of how well model outputs represent participants' views \cite{poole-dayanBenchmarkingOvertonPluralism2025}. Our study instead measures recovery of fixed, externally documented reference perspectives in matched WEIRD and Serbian controversies. The contribution is this matched comparison across settings. Differences in reference construction and scoring preclude direct comparison of absolute scores between the two benchmarks.

\subsection{Evaluating generated perspectives}
\label{sec:Evaluating generated perspectives}
Evaluating coverage requires deciding whether differently worded statements express the same stance. LLM judges can assess this relationship, but their agreement with human assessments can vary across the models being evaluated \cite{poole-dayanBenchmarkingOvertonPluralism2025}.

We use five judges, present each generated perspective separately, randomise reference order, and exclude judges from the generator's model family. We also report inter-judge agreement and compare it across WEIRD and Serbian topics. These checks assess consistency of the matching procedure. They cannot establish correctness, because several judges may share an error, and they do not replace human validation.

\section{Methodology}
````

### With this

````latex
\section{Related work}
\label{sec:Related work}
\subsection{Pluralistic alignment and cultural representation}
\label{sec:Pluralistic alignment and cultural representation}
Pluralistic alignment seeks to preserve differences in human values and viewpoints rather than collapse them into one preference target \cite{sorensenRoadmapPluralisticAlignment2024,fengModularPluralismPluralistic2024,aliOperationalizingPluralisticValues2025}. Our benchmark measures Overton-style coverage: whether documented positions are recovered at all, rather than whether a model can adopt a requested stance or reproduce population frequencies \cite{sorensenRoadmapPluralisticAlignment2024}.

The concentration of data and evaluation in WEIRD and English-language settings motivates concern about uneven cultural representation \cite{sorensenRoadmapPluralisticAlignment2024,wangMultilingualPromptingImproving2025,zewailMoralStereotypingLarge2026}. Multilingual prompting can improve diversity in some settings \cite{wangMultilingualPromptingImproving2025}, while Serbian SuperGLUE addresses gaps in Serbian language-understanding evaluation \cite{perovicSerbianSuperGLUEEvaluation2026}. These concerns motivate our directional hypothesis, but topic selection may also affect observed coverage.

\subsection{Measuring and evaluating perspective coverage}
\label{sec:Measuring perspective coverage}
Political controversies rarely have exhaustive, uncontested labels. Perspectivist NLP treats disagreement as part of the phenomenon \cite{basileWeNeedConsider2021,plankProblemHumanLabel2022a,frendaPerspectivistApproachesNatural2025a}; related approaches retain annotator rationales or label distributions \cite{sarumiFineGrainedPerspectivesModeling2026,shettyLearningWhoDisagrees2026}. LLM simulations of opinion and hybrid annotation approaches offer other evaluation routes, but their outputs depend on prompting and methodology \cite{sunRandomSiliconSampling2024,gongCharacterizingAbilityLLMs2026,khanRandomnessNotRepresentation2025,mehrotraMultiPerspectiveLLMAnnotations2026}.

The closest benchmark, OvertonBench, evaluates viewpoint coverage using human responses and ratings of how well outputs represent participants' views \cite{poole-dayanBenchmarkingOvertonPluralism2025}. We instead compare recovery of fixed, externally documented reference perspectives across matched WEIRD and Serbian controversies. Differences in reference construction and scoring preclude direct comparison of absolute scores. LLM judging makes stance matching practical, but agreement with human assessments can vary across evaluated models \cite{poole-dayanBenchmarkingOvertonPluralism2025}. We therefore report judge consistency and sensitivity to panel membership, without treating these checks as validation of correctness.

\section{Methodology}
````

## Swap 18 — Redirect supplementary precision and F1 reporting

**Original lines:** [188–192](/Users/vuk/Downloads/0_version_2.tex:188). **Revised lines:** [188–192](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/shortened_manuscript.tex:188).

### Replace this

````latex
\textit{How do the selected models from US and Chinese developers differ in overall recall and in their WEIRD-Serbian recall gaps?}

Recall is the principal outcome because all three questions concern recovery of documented perspectives. Precision and F1 provide supplementary descriptions of matching behaviour. The category and developer-country comparisons are exploratory. The model categories describe access and relative size, not a capability ranking.

We do not detect the predicted WEIRD advantage. Mean recall is $0.581$ for WEIRD topics and $0.594$ for Serbian topics, with four matched pairs favouring each side. Coverage nevertheless remains incomplete. Even the highest-recall model misses roughly three of every ten reference perspectives on average.
````

### With this

````latex
\textit{How do the selected models from US and Chinese developers differ in overall recall and in their WEIRD-Serbian recall gaps?}

Recall is the principal outcome because all three questions concern recovery of documented perspectives. Supplementary precision and F1 results are retained in the accompanying analysis files. The category and developer-country comparisons are exploratory. The model categories describe access and relative size, not a capability ranking.

We do not detect the predicted WEIRD advantage. Mean recall is $0.581$ for WEIRD topics and $0.594$ for Serbian topics, with four matched pairs favouring each side. Coverage nevertheless remains incomplete. Even the highest-recall model misses roughly three of every ten reference perspectives on average.
````

## Completeness check

The replacements in this Markdown file were applied back to a copy of the original source, in the order shown. The result was checked against `shortened_manuscript.tex` and matched **byte for byte**. The manuscript itself has not been changed again for this guide.

The existing [CHANGE_GUIDE.md](/Users/vuk/Downloads/BWEIRD/output/pdf/simplified_kappa_revision/CHANGE_GUIDE.md) provides the shorter explanation of why each change was made and the original PDF page locations.
