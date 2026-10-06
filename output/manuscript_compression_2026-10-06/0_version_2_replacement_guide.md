# Replacement guide: shorten 0_version_2.tex

**Source:** [0_version_2.tex](/Users/vuk/Downloads/paper/0_version_2.tex). Original snapshot: 1,060 lines; SHA-256 `4ede3b60a911ca52572a632bc880f13af69359c2bead0d4a9f41c963ca38a032`.

**Delivery boundary:** this is a Markdown editing guide. No TeX source, README, or GitHub content has been edited. All LaTeX blocks below are proposed text for you to paste.

Use the searchable anchors as the primary locations. Line numbers refer to the untouched source and will shift after edits. Each requested table move includes the complete table, so you do not need to recover it from a deleted block. Apply the guide once; do not paste moved tables twice.

## Two corrections needed before applying the requested cuts

1. **The group comparisons do not all fail Holm correction.** None of the four model-category comparisons reaches the adjusted 0.05 threshold, but the US–China overall-recall contrast has adjusted p = 0.046875, reported as 0.047. The developer-country cultural-gap contrast has adjusted p = 0.453. The guide retains this distinction, with the existing correction families (four category tests and two country tests); it does not change the statistical analysis to obtain a different conclusion.
2. **The appendix letters in the request belong to a different layout.** In this file, aggregation is A.3, the worked example is E, and execution identifiers are F. Tables 5, 10, 11, and 12 match the requested titles. Use the labels below, not hard-coded letters or table numbers. The supplied `.aux` agrees with these appendix letters.

## 1. Merge Results 4.2 and 4.3

The replacement has exactly three prose sentences, followed by the existing model-level Table 4, unchanged. Only the developer-group table moves out of the main text, as requested. The old RQ2 and RQ3 labels remain as aliases for the merged subsection, so the existing reference to `sec:rq2` still resolves.

### 1A. Replace both exploratory results subsections

**Where:** original lines **463–524** in [0_version_2.tex](/Users/vuk/Downloads/paper/0_version_2.tex:463).

Stop before `\subsection{Judge Reliability and Cross-Cultural Consistency}`. The displayed p-values remain Holm-adjusted under the existing Methods statement. LaTeX will number the merged subsection 4.2; judge reliability becomes 4.3 and judge disagreement becomes 4.4.

**Replace the complete block beginning with:**

```latex
\subsection{RQ2: Recall by model and access category}
\label{sec:rq2}
```

**Through its final line, inclusive:**

```latex
The groups differ in composition. The Chinese group contains one Frontier model and three larger open-weight models; the US group contains four Frontier, two larger open-weight, and two smaller open-weight models. Only the US group includes smaller open-weight systems. Excluding them reduces the observed overall US-minus-China difference from $-3.0$ to about $-2.0$ percentage points. Some US developers also contribute more than one model. These comparisons consequently describe the selected systems and cannot establish that Chinese models generally perform better or that developer country causes the observed difference.
```

**With:**

```latex
\subsection{Exploratory Group Comparisons}
\label{sec:exploratory-groups}
\label{sec:rq2}
\label{sec:rq3}
Mean recall was $0.615$ for Frontier/API systems, $0.578$ for larger open-weight systems, and $0.548$ for smaller open-weight systems ($0.570$ across all open-weight models; Table~\ref{tab:model-recall}). No model-category comparison survived Holm correction, whereas overall recall differed between US ($0.579$) and Chinese ($0.609$) developer groups ($p=0.047$); their WEIRD--Serbian gaps did not differ detectably ($p=0.453$). These exploratory comparisons do not isolate effects of size, openness, or developer country; Appendices~\ref{app:category-tests} and~\ref{app:country-tests} report the detailed results and composition caveats.

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

### 1B. Align the introduction’s RQ2 heading

**Where:** original lines **184–184** in [0_version_2.tex](/Users/vuk/Downloads/paper/0_version_2.tex:184).

Keep the research-question wording and all three RQs. This small heading change matches the demoted status of the group comparisons.

**Find this exact text:**

```latex
\paragraph{RQ2 (secondary).}
```

**With:**

```latex
\paragraph{RQ2 (exploratory).}
```

## 2. Move the developer table and retain the important caveats in the appendix

### 2A. Append the developer table to the existing developer-country subsection

**Where:** immediately before original line **788** in [0_version_2.tex](/Users/vuk/Downloads/paper/0_version_2.tex:788).

**Unique anchor; retain it after the insertion:**

```latex
\subsection{Pairwise model comparisons}
\label{app:model_pair_tests}
```

This is inside `\subsection{Exploratory developer-country comparisons}` (`app:country-tests`, currently B.5), after the paragraph ending “The accompanying analysis files contain both contrasts and their uncertainty estimates.” Retain the existing test description, confidence intervals, raw p-values, and Holm-adjusted p-values. The table is copied verbatim from the original main text; retain its `tab:origin-recall` label.

**Insert:**

```latex
Table~\ref{tab:origin-recall} reports the descriptive group means.

\begin{table}[!htbp]
\centering
\small
\caption{Recall by developer group. Models receive equal weight within each group. Mistral is excluded from this US-China contrast. A positive WEIRD-Serbian gap indicates higher recall on WEIRD topics.}
\label{tab:origin-recall}
\setlength{\tabcolsep}{3pt}
\begin{tabular*}{\columnwidth}{@{\extracolsep{\fill}}lccccc@{}}
\toprule
Group & $n$ & Overall & WEIRD & Serbian & Gap\\
\midrule
US & 8 & $0.579$ & $0.570$ & $0.589$ & $-0.019$\\
China & 4 & $0.609$ & $0.613$ & $0.606$ & $+0.006$\\
\bottomrule
\end{tabular*}
\end{table}

The groups differ in composition. The Chinese group contains one Frontier model and three larger open-weight models; the US group contains four Frontier, two larger open-weight, and two smaller open-weight models. Only the US group includes smaller open-weight systems. Excluding them reduces the observed overall US-minus-China difference from $-3.0$ to about $-2.0$ percentage points. Some US developers also contribute more than one model. These comparisons consequently describe the selected systems and cannot establish that Chinese models generally perform better or that developer country causes the observed difference.
```

### 2B. Retain the model-panel caveat in the category appendix

**Where:** immediately before original line **780** in [0_version_2.tex](/Users/vuk/Downloads/paper/0_version_2.tex:780).

**Unique anchor; retain it after the insertion:**

```latex
\subsection{Exploratory developer-country comparisons}
\label{app:country-tests}
```

Append this to `app:category-tests` (currently B.4), after its existing results paragraph. This preserves the judge-strictness caution that would otherwise disappear when the original RQ2 subsection is cut.

**Insert:**

```latex
Model categories do not isolate size, openness, or capability. Panel composition also complicates comparisons: Gemini 3.1 Pro matched $52.7\%$ of the outputs it judged, compared with $65.0$--$76.6\%$ for the other judges, and removing it raises individual-model recall by up to $3.6$ percentage points (Appendix~\ref{app:lojo}). Google's two generators are never scored by this judge under the family-disjoint design, so small differences between their scores and those of other generators require caution.
```

## 3. Replace the recall tutorial with compact prose

The three-step walkthrough and all equations within Section 3.3.3 are removed. The primary matched-pair equations in Section 3.3.4 stay. The replacement explicitly retains duplicate splitting before averaging: merely averaging raw matches and capping afterwards would not fully describe the implemented calculation.

### 3A. Replace Section 3.3.3 completely

**Where:** original lines **357–418** in [0_version_2.tex](/Users/vuk/Downloads/paper/0_version_2.tex:357).

Keep the following `Comparisons and statistical analysis` subsection. The automatic appendix reference resolves to A.3 in this file and will follow any later renumbering.

**Replace the complete block beginning with:**

```latex
\subsubsection{From assignments to recall}
\label{sec:recall}
```

**Through its final line, inclusive:**

```latex
Appendix~\ref{app:prf-results}.
```

**With:**

```latex
\subsubsection{From assignments to recall}
\label{sec:recall}
Recall measures the proportion of a topic's five reference perspectives recovered by a model's five outputs. Duplicate matches to the same reference share one unit of credit within each judge. These fractional credits are averaged over valid judges for each output, summed by reference, capped at one per reference, and averaged across the five references. Missing judgements are excluded, while valid no-match decisions contribute zero credit; no majority-vote threshold is applied. Model and topic summaries give equal weight to topics and models, respectively. Appendix~\ref{app:recall_aggregation} gives the exact fractional-credit formulas; precision and F1 are defined in Appendix~\ref{app:precision_aggregation} and reported in Appendix~\ref{app:prf-results}.
```

### 3B. Remove the appendix’s pointer to the deleted main-text equation

**Where:** original lines **676–676** in [0_version_2.tex](/Users/vuk/Downloads/paper/0_version_2.tex:676).

This is the final paragraph of `app:recall_aggregation`, immediately before the `Precision` subsection. Keep the three existing fractional-credit equations unchanged. The replacement removes the dangling reference to `eq:mean-judge-recall`.

**Find this exact text:**

```latex
With complete panels, these equations reduce to the mean judge recall in Eq.~\ref{eq:mean-judge-recall}. When judgments are missing, $|J_k|$ can differ across outputs; the cap prevents any reference receiving more than full credit. All outputs in this dataset have at least four valid judgments.
```

**With:**

```latex
With complete panels, these equations equal the mean, across the five judges, of the proportion of distinct references each judge recovers. When judgements are missing, $|J_k|$ can differ across outputs; the cap prevents any reference receiving more than full credit. All outputs in this dataset have at least four valid judgements.
```

## 4. Condense Related work to two paragraphs

Remove all three subsection headings and their unused labels. The replacement preserves every distinct citation key used in the original Related work section, removes the textbook taxonomy, and retains the distinction from OvertonBench and the limits of LLM judging.

### 4A. Replace the complete Related work section

**Where:** original lines **202–226** in [0_version_2.tex](/Users/vuk/Downloads/paper/0_version_2.tex:202).

Stop before `\section{Methodology}`. The replacement contains the same section heading and section label, followed by exactly two paragraphs.

**Replace the complete block beginning with:**

```latex
\section{Related work}
\label{sec:Related work}
```

**Through its final line, inclusive:**

```latex
We use five judges, present each generated perspective separately, randomise reference order, and exclude judges from the generator's model family. We also report inter-judge agreement and compare it across WEIRD and Serbian topics. These checks assess consistency of the matching procedure. They cannot establish correctness, because several judges may share an error, and they do not replace human validation.
```

**With:**

```latex
\section{Related work}
\label{sec:Related work}
Our benchmark evaluates Overton-style coverage of externally documented perspectives \cite{sorensenRoadmapPluralisticAlignment2024}, asking whether models recover fewer positions on Serbian controversies than on structurally matched WEIRD topics. Pluralistic alignment seeks to preserve differing values and viewpoints \cite{fengModularPluralismPluralistic2024, aliOperationalizingPluralisticValues2025}, but cross-cultural coverage remains difficult to separate from topic selection. Work on multilingual prompting and moral stereotyping motivates this concern \cite{wangMultilingualPromptingImproving2025, zewailMoralStereotypingLarge2026}, while Serbian SuperGLUE illustrates gaps in South Slavic evaluation resources \cite{perovicSerbianSuperGLUEEvaluation2026}. The closest benchmark, OvertonBench, assesses coverage using viewpoint groups derived from human responses and ratings of how well outputs represent participants' views \cite{poole-dayanBenchmarkingOvertonPluralism2025}. We instead compare matched controversies against fixed, externally documented references; differences in reference construction and scoring preclude direct comparison of absolute scores.

Perspectivist NLP treats disagreement as part of the phenomenon being studied \cite{basileWeNeedConsider2021, plankProblemHumanLabel2022a, frendaPerspectivistApproachesNatural2025a}, retaining annotator-specific rationales or label distributions \cite{sarumiFineGrainedPerspectivesModeling2026, shettyLearningWhoDisagrees2026}. LLM-based opinion simulation can reproduce some polling patterns \cite{sunRandomSiliconSampling2024, gongCharacterizingAbilityLLMs2026}, but its results depend on prompting and methodology \cite{khanRandomnessNotRepresentation2025}; hybrid annotation approaches direct human attention to uncertain cases \cite{mehrotraMultiPerspectiveLLMAnnotations2026}. Our references keep the scoring target separate from the evaluated models, without claiming to exhaust legitimate positions. Five family-disjoint judges, randomised reference order, and agreement checks assess matching consistency, but cannot establish correctness or replace human validation.
```

## 5. Remove the worked-example appendix and its two tables

Delete the whole worked example (currently Appendix E; called G in the request). This removes Tables 10 and 11. Retain the earlier reference-set table `tab:reference-example`: it is a different table and remains useful when defining the benchmark. Do not add another main-text example table; the existing disagreement prose supplies the necessary illustration.

### 5A. Delete the worked-example block, including its introductory comments

**Where:** original lines **964–1024** in [0_version_2.tex](/Users/vuk/Downloads/paper/0_version_2.tex:964).

The deletion includes `app:worked-example`, `tab:fracking-outputs`, `tab:fracking-matches`, both minipages, the complete `table*` environment, and the final worked recall calculation. Stop immediately before the execution appendix heading; that appendix is handled separately in Edit 6A.

**Replace the complete block beginning with:**

```latex
% Real example extracted from saved benchmark and evaluation records.
% Sources and provenance are documented in example_evidence.md.
```

**Through its final line, inclusive:**

```latex
Equivalently, the five reference credits are $(1,1,0,0,0.8)$. Their mean is $0.56$. No majority-vote threshold is applied: reference 5 receives fractional credit reflecting its recovery by four judges. Reference 2 receives full credit because all five judges recover it through output 1; the extra match from output 2 does not increase its credit.
```

**Delete the entire block; insert nothing in its place.**

### 5B. Remove the duplicated fracking explanation from the methodology

**Where:** original lines **348–348** in [0_version_2.tex](/Users/vuk/Downloads/paper/0_version_2.tex:348).

This is the second paragraph of `Judge assignments`. The new pointer follows the disagreement subsection automatically when it becomes Section 4.4.

**Find this exact text:**

```latex
For example, all five judges matched a GPT 5.5 output supporting UK fracking for energy security, jobs, and reduced import dependence to reference 1 in Table~\ref{tab:reference-example}. A different output opposed fracking because it distrusted companies and regulators. Claude Sonnet~5 matched it to reference 2, whereas the other four judges returned no match. This disagreement concerns correspondence to the reference set, not whether the output expresses a legitimate position. Appendix~\ref{app:worked-example} shows the saved outputs and all assignments. Judges evaluated both summaries and explanations.
```

**With:**

```latex
Judges evaluated both the summary and explanation of each generated and reference perspective. Section~\ref{sec:judge-disagreement} discusses examples of disputed matches.
```

### 5C. Point the disagreement subsection to the repository

**Where:** original lines **538–538** in [0_version_2.tex](/Users/vuk/Downloads/paper/0_version_2.tex:538).

Append one sentence to the final paragraph of `sec:judge-disagreement`; retain both examples and their vote counts. The README block below identifies the exact data files.

**Find this exact text:**

```latex
The recorded explanations suggest that the judges differed in how they interpreted the boundaries of a stance, including its rationale and conditions for support. These cases illustrate a source of semantic disagreement, but do not establish its prevalence across the dataset or rule out hallucinations and other judgement errors.
```

**With:**

```latex
The recorded explanations suggest that the judges differed in how they interpreted the boundaries of a stance, including its rationale and conditions for support. These cases illustrate a source of semantic disagreement, but do not establish its prevalence across the dataset or rule out hallucinations and other judgement errors. The repository contains the full generated perspectives, reference texts, and judge decisions for these examples.
```

## 6. Move execution identifiers and configuration details to the README

Remove the execution appendix (currently F; called H in the request), including Table 12. Its response counts and collection dates already appear in the methodology. Its endpoint identifiers, release-source links, and configuration details are retained in the README block in Section 8 of this guide.

### 6A. Delete the execution appendix

**Where:** original lines **1026–1058** in [0_version_2.tex](/Users/vuk/Downloads/paper/0_version_2.tex:1026).

**Keep `\end{document}`.** This removes `app:execution` and `tab:model-identifiers`, so the two main-text pointers must also be changed below.

**Replace the complete block beginning with:**

```latex
\section{Execution records and model identifiers}
\label{app:execution}
```

**Through its final line, inclusive:**

```latex
The release sources used for the public-weight categories are the published pages for \href{https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro}{DeepSeek V4 Pro}, \href{https://huggingface.co/moonshotai/Kimi-K2.6}{Kimi K2.6}, \href{https://huggingface.co/zai-org/GLM-5.2}{GLM 5.2}, \href{https://huggingface.co/collections/mistralai/mistral-large-3}{Mistral Large 3}, \href{https://ai.meta.com/llama/get-started/}{Meta's Llama models}, \href{https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/}{Gemma 4}, and \href{https://huggingface.co/openai/gpt-oss-120b}{GPT-OSS 120B}. The smaller group contains the selected 31B and 70B systems; the label is relative to the larger public-weight systems in this selection. It does not imply a common active-parameter count, runtime cost, licence, or training-data disclosure.
```

**Delete the entire block; insert nothing in its place.**

### 6B. Replace the execution-table pointer in Models and perspective generation

**Where:** original lines **310–310** in [0_version_2.tex](/Users/vuk/Downloads/paper/0_version_2.tex:310).

This is the last sentence of the paragraph beginning “All generator prompts, judge prompts, and reference statements are in English.” Retain all reported settings, collection dates, and sampling limitations in that paragraph.

**Find this exact text:**

```latex
Appendix~\ref{app:execution} lists the configured model identifiers.
```

**With:**

```latex
Configured model identifiers and API settings are documented in the repository README.
```

### 6C. Replace the category-provenance pointer and fix the adjacent grammar

**Where:** original lines **312–312** in [0_version_2.tex](/Users/vuk/Downloads/paper/0_version_2.tex:312).

This is the final two sentences of the paragraph beginning “For the exploratory category comparison”. Retain its definitions, counts, and Qwen commercial-model footnote.

**Find this exact text:**

```latex
Appendix~\ref{app:execution} records category membership and release-source links. The exact system prompts, including the JSON schemas enforcing the zero-shot generation is available in the project repository.
```

**With:**

```latex
Category membership, release-source links, and the exact generation prompt and JSON schema are documented in the repository README.
```

## 7. Repair an adjacent reference that is already unresolved in this source

The file references `app:generator_prompt`, but defines no such label and includes no external TeX file supplying it. Since the prompts are in the repository, replace this existing broken appendix pointer as follows.

### 7A. Replace the missing generation-prompt appendix reference

**Where:** original lines **308–308** in [0_version_2.tex](/Users/vuk/Downloads/paper/0_version_2.tex:308).

**Find this exact text:**

```latex
Appendix~\ref{app:generator_prompt} reproduces the prompt.
```

**With:**

```latex
The generation prompt and output schema are provided in the project repository.
```

## 8. Paste-ready README addition

**Destination:** the repository’s `README.md` (local copy: [README.md](/Users/vuk/Downloads/BWEIRD/README.md)). Insert this block immediately before the existing `## Checkpointing and failure semantics` heading. This is proposed text only; neither the local README nor GitHub has been edited.

The seed and request defaults below were checked in the local runner. Endpoint strings and collection dates are recorded study identifiers, not a new audit of external model releases. The release links reproduce the supplied manuscript’s source links.

````markdown
## Execution configuration and saved records

The study queried generators and judges through the OpenRouter chat-completions API. The configuration files and request builder define the execution settings:

- [Generator configuration](config/models.json): model identifiers and developer-family labels.
- [Judge configuration](config/judges.json): the base panel and family-disjoint substitutions.
- [Prompt templates and output schemas](bweird/prompts.py): generation and matching prompts.
- [API request builder](bweird/openrouter.py): configured request parameters and retry handling.

| Parameter | Configured value |
|---|---|
| API endpoint | `https://openrouter.ai/api/v1/chat/completions` |
| Temperature | `0.0` |
| Completion-token limit | `4096` |
| Request seed | `20260708`, effective only where the provider supports seeded sampling |
| Reference-order randomisation seed | `20260708` by default; combined with each execution key to generate an independent reproducible shuffle |
| Reasoning parameters | Not explicitly set |
| Provider routing | OpenRouter default routing; providers were not pinned |
| Serving-provider identity | Not recorded |
| Prompt and reference language | English |

The runner allows one repair request for an unparseable response and retries transient failures. Valid responses are saved and reused. Failed judging calls remain in the append-only log; later retry records supersede earlier records for the same execution. A missing decision is distinct from a valid no-match decision.

### Configured generator identifiers

These are the exact endpoint strings stored in the study configuration. Categories describe access and relative size within this model selection, not a capability ranking.

| Model | Category | Configured endpoint |
|---|---|---|
| Claude Opus 4.8 | Frontier/API | `anthropic/claude-opus-4.8` |
| GPT 5.5 | Frontier/API | `openai/gpt-5.5` |
| Gemini 3.1 Pro Preview | Frontier/API | `google/gemini-3.1-pro-preview` |
| Grok 4.3 | Frontier/API | `x-ai/grok-4.3` |
| DeepSeek V4 Pro | Larger open-weight | `deepseek/deepseek-v4-pro` |
| Qwen 3.7 Max | Frontier/API | `qwen/qwen3.7-max` |
| Kimi K2.6 | Larger open-weight | `moonshotai/kimi-k2.6` |
| GLM 5.2 | Larger open-weight | `z-ai/glm-5.2` |
| Llama 4 Maverick | Larger open-weight | `meta-llama/llama-4-maverick` |
| Mistral Large 3 | Larger open-weight | `mistralai/mistral-large-2512` |
| GPT-OSS 120B | Larger open-weight | `openai/gpt-oss-120b` |
| Gemma 4 31B | Smaller open-weight | `google/gemma-4-31b-it` |
| Llama 3.3 70B | Smaller open-weight | `meta-llama/llama-3.3-70b-instruct` |

### Judge identifiers and substitutions

The base panel comprises `google/gemini-3.1-pro-preview`, `openai/gpt-5.5`, `anthropic/claude-sonnet-5`, `deepseek/deepseek-v4-pro`, and `moonshotai/kimi-k2.6`. A same-family judge is replaced by `x-ai/grok-4.5` for Google, OpenAI, Anthropic, or Moonshot generators, and by `qwen/qwen3.7-max` for DeepSeek generators. The five final judges are from distinct families and none shares the generator’s configured family.

### Saved records and collection window

- [Generated perspectives](data/outputs/generations.jsonl): 208 unique model-topic responses containing 1,040 perspectives. Every retained response contains five perspectives, although the prompt permitted fewer. Retained responses are not a count of API requests.
- [Judge records](data/outputs/judgments.jsonl): 5,228 raw records, including failed calls and retries. Resolving retries yields 5,184 valid decisions out of 5,200 intended decisions; 16 remain missing.
- [Reference perspectives](data/gold_standard.json) and [topic definitions](data/topics.json): the fixed scoring targets and matched topics.
- Generation timestamps: 9–10 July 2026 UTC. Judgement timestamps, including retries: 10–20 July 2026 UTC.

The disagreement examples can be located by `model_slug`, `topic_id`, and perspective `index` in the generation file, and by `generator_slug`, `topic_id`, and `gen_index` in the judgement file. The UK fracking example is `openai/gpt-5.5`, `pair03_weird`, perspective 2; the Jadar supply-chain example is `google/gemini-3.1-pro-preview`, `pair03_serbian`, perspective 4. Use the final record per judge and execution, and use the canonical `match_gold_id` rather than the shuffled `match_presented` index. Original summaries, explanations, assignments, and judge justifications remain available for inspection.

### Sources used for the manuscript’s access categories

The manuscript cites the following release pages for its public-weight classifications:

- [DeepSeek V4 Pro](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro)
- [Kimi K2.6](https://huggingface.co/moonshotai/Kimi-K2.6)
- [GLM 5.2](https://huggingface.co/zai-org/GLM-5.2)
- [Mistral Large 3](https://huggingface.co/collections/mistralai/mistral-large-3)
- [Meta Llama models](https://ai.meta.com/llama/get-started/)
- [Gemma 4](https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/)
- [GPT-OSS 120B](https://huggingface.co/openai/gpt-oss-120b)

The Frontier/API classification of Qwen 3.7 Max follows the manuscript’s cited [commercial-model announcement](https://www.alibabacloud.com/en/news/product/maxcompute-model-computing-service-supports-qwen37-max-and-other-commercial-models-mkv). The smaller open-weight group comprises the selected 31B and 70B systems. This relative grouping does not imply common active-parameter counts, runtime costs, licences, or training-data disclosure.
````

## 9. What changes automatically, and what still needs attention

- **Results numbering:** RQ1 remains 4.1; Exploratory Group Comparisons becomes 4.2; Judge Reliability becomes 4.3; Analysis of Judge Disagreement becomes 4.4. Do not type these numbers into headings or references.
- **Appendices:** Evaluation details, Statistical details, Secondary results, and Judge reliability remain A–D. The worked-example and execution appendices are removed. The moved developer table is inside the existing statistical appendix, not a new appendix.
- **Tables:** the developer table’s number and later table numbers change automatically. Retain `tab:origin-recall`; remove the three deleted table labels. The model-level recall table and the reference-set example remain.
- **Equations:** only the main-text recall walkthrough equations are deleted. The exact fractional-credit equations in A.3 and the primary cultural-comparison equations remain. Subsequent equation numbers update automatically.
- **Repository address:** the Data and code availability section still says that the final repository or archival identifier will be added. Supply the actual public URL/DOI before relying on repository pointers in a released manuscript; no address has been invented here.
- **Existing template reference:** `sec:contributors` is referenced in the template author block but is not defined. It predates these changes and is outside this shortening guide; replace the template author metadata separately.
- **Page savings:** the requested page reductions are estimates. No revised TeX was written or compiled, so pagination, float placement, and exact page savings have not been verified.

## 10. Verification of this guide

- All **14** replacement/insertion locations matched unique anchors in the supplied source, and no edit ranges overlap.
- Applied the proposed changes to an in-memory copy to check structure; no temporary or revised TeX file was created.
- The moved developer table and retained model table are byte-for-byte identical to their original blocks, each appearing once in the proposed layout.
- All **21** distinct citation keys from the manuscript remain; all **16** distinct Related work citation keys are preserved.
- The exploratory main-text summary has exactly three sentences; Related work has exactly two paragraphs.
- No duplicate labels or new unresolved cross-references were introduced. The pre-existing generation-prompt reference is repaired; only the pre-existing author-template `sec:contributors` reference remains.
- The removed appendix/table/equation labels have no surviving pointers; exact fractional-credit and primary-test equations remain.
- Checked balanced LaTeX environments in the in-memory result. This is a structural check, not a successful compilation or visual layout check.
- Verified the source SHA-256 is unchanged. The guide is the only manuscript deliverable.

**Statistical cross-check:** the supplied manuscript reports the country contrast at original lines 504 and 786. The saved [developer-country results](/Users/vuk/Downloads/BWEIRD/output/pdf/version_3/supplementary/developer_country_contrasts.csv:2) give adjusted p = 0.046875 for overall recall and 0.453125 for the cultural gap. The compression preserves these reported tests rather than redefining the correction family.
