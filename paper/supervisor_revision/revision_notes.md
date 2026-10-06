# Revision in response to the supervisor

The requested change is to make the paper's argument and evaluation sequence explicit: define the matching task, explain recall, then organize the results as RQ1 (WEIRD versus Serbian), RQ2 (model performance and categories), RQ3 (US versus China), followed by descriptive judge checks.

This pack contains replacement passages, not a reconstruction of the entire manuscript. The supplied PDF remains unchanged. The original main result and original model-level recall confidence intervals are preserved. Arm-specific recall values, category summaries, and new sensitivity analyses were calculated from the saved scores, without generating new model responses or judgments.

## What each comment changes

| Supervisor comment | Revision |
|---|---|
| Improve the mean-difference sentence | State the subtraction direction, identify the eight pairs, explain the size in percentage points, then state the test result. |
| What happens first when judges evaluate? | A judge assigns each output to one reference or no match. Scores are calculated only after these assignments have been collected. |
| Define family-disjoint judging | No judge shares the generator's configured developer family. Google includes Gemini and Gemma; OpenAI includes GPT and GPT-OSS. |
| Explain recall separately | Add a dedicated recall subsection with a five-output example, a five-judge example, and the exact missing-judgment formula. |
| Make the cultural result RQ1 | Use the heading “RQ1: Recall on matched WEIRD and Serbian topics.” |
| Remove precision and F1 from the main model table | Show overall, WEIRD, and Serbian recall; group the rows and sort by recall within each group. Keep the old precision/F1 material in an appendix. |
| Improve open versus closed comparison | Use five Frontier/API systems, six larger open-weight systems, and two smaller open-weight systems; move Qwen Max to the API group with a source note. |
| Add US versus China | Add an explicitly exploratory RQ3 with country-group means and a separate comparison of their cultural gaps. |
| Keep judge reliability descriptive | Put agreement, no-match rates, and judge-removal checks last. Interpret them as checks on consistency and sensitivity, not proof of unbiased or correct judgments. |

## The scoring sequence, in plain language

For one model and one topic, put the **five generated perspectives** in five rows. Put the **five reference perspectives** in five columns. Each judge assigns every generated perspective to one reference column, or to no match. That produces 25 matching decisions when all five judges respond.

For a single judge, assignments `1, 2, 2, 4, no match` cover three distinct references. That judge's recall is `3/5 = 0.60`. The second assignment to reference 2 does not cover a new perspective. Precision would be `4/5 = 0.80`, because four outputs matched something. This makes recall the direct measure of omission from the reference set.

With complete panels, calculate this distinct-reference recall for each judge and average the five recalls. That is mathematically equivalent to the implemented fractional-credit aggregation. For example, five recalls of `0.60, 0.60, 0.80, 0.40, 0.40` give topic recall `0.56`.

There is one qualification: **16 outputs have four valid judgments rather than five**. The implementation handles missing judgments separately for each output, so a simple unqualified “average the five judge recalls” would not reproduce every score. The exact sequence is:

1. Split a judge's one unit of credit among that judge's duplicate matches to the same reference.
2. Average those credits over the valid judges for each output.
3. Sum the credits for each reference, with a maximum of one.
4. Average the five reference credits to obtain topic recall.
5. Average 16 topic scores for overall model recall, or eight scores for each cultural arm.

Failed calls are missing; valid no-match decisions earn zero and remain in the denominator. The cap is actually used twice in the saved data. The replacement equations preserve this behavior.

## RQ1: three views of the paired data

Define `d[m,p] = recall_WEIRD[m,p] - recall_Serbian[m,p]`. Every row of the 13 × 8 matrix represents a generator and every column a matched topic pair.

| Analysis | Input | Result | Interpretation |
|---|---|---|---|
| Original primary test | Eight pair means, averaging the 13 models within each pair | Mean −0.013; original 95% CI [−0.081, 0.058]; one-sided exact signed-rank p = 0.680 | Tests the predicted WEIRD advantage across these matched controversies. |
| New model-mean sensitivity | Thirteen model means, averaging eight pairs within each model | One-sided p = 0.843; two-sided p = 0.331 | Conditional on the same topics; shared model families also limit independence. |
| New joint sensitivity | All 104 gaps with crossed model and pair effects | Mixed-model estimate −0.013; SE 0.038; two-sided Wald p = 0.733; CI [−0.088, 0.062] | Approximate inference under the random-effects assumptions. |
| New crossed bootstrap | Independently resample model rows and pair columns | 95% CI [−0.090, 0.070] | Approximate uncertainty over both observed dimensions; no bootstrap p-value is claimed. |

Do not flatten the matrix and run an ordinary Wilcoxon test on 104 supposedly independent gaps. Cells share generators and topic pairs. The [SciPy signed-rank documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.wilcoxon.html) specifies independence assumptions and explains why numerical ties need care. The model-mean test uses midranks and all 8,192 sign assignments; two model gaps are exactly −0.020 after numerical noise is removed.

The crossed model follows the [statsmodels variance-component specification](https://www.statsmodels.org/stable/examples/notebooks/generated/variance_components.html). It converged; an independent balanced variance calculation and a second optimizer reproduced its estimates. The model variance is small but positive, and the optimizer reports a boundary warning. Report it as a sensitivity analysis. The bootstrap follows [Owen's pigeonhole bootstrap](https://arxiv.org/abs/0712.1111), with 10,000 resamples and seed 42. Neither analysis makes the purposively selected models or topics representative of all models or cultures; neither explicitly models dependence between different generators from one developer family.

The figure `paired_recall.png` shows all three levels while preserving the pairing. The 104 raw gaps comprise 46 positive, 51 negative, and seven zero values. These are descriptive counts, not 104 independent replications.

## RQ2: access categories, with Qwen Max moved out of the open group

The revised main table uses **Frontier/API (5), Open-weight (6), and Small open-weight (2)**. It preserves all 13 models and their scores. Qwen 3.7 Max moves into the API group, rather than inheriting the original middle tier's open-weight label. This is an explicit classification change in response to the requested open-versus-closed comparison.

The [official Qwen platform](https://qwen.ai/apiplatform) lists the Max endpoint as a flagship, and [Alibaba's announcement specifically identifies Qwen3.7-Max as a commercial model](https://www.alibabacloud.com/en/news/product/maxcompute-model-computing-service-supports-qwen37-max-and-other-commercial-models-mkv). A public-weight release for the evaluated Max endpoint was not verified. The manuscript therefore uses the operational label “Frontier/API,” rather than claiming that “frontier” inherently means closed or that no public release could ever exist.

Public release evidence is available for [DeepSeek V4 Pro](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro), [Kimi K2.6](https://huggingface.co/moonshotai/Kimi-K2.6), [GLM 5.2](https://huggingface.co/zai-org/GLM-5.2), [Mistral Large 3](https://huggingface.co/collections/mistralai/mistral-large-3), [Meta's Llama models](https://ai.meta.com/llama/get-started/), [Gemma 4](https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/), and [GPT-OSS 120B](https://huggingface.co/openai/gpt-oss-120b). The two smaller systems are Gemma 31B and Llama 70B; “small” is relative to the other public-weight models in this selection, not a claim about active parameters, runtime cost, or deployment on small devices.

“Open-weight” concerns weight availability. It does not imply identical licenses, training-data disclosure, compute requirements, or capability. All generators were evaluated through the same API-based workflow, so this is a comparison of model access categories, not local versus hosted execution.

| Revised category | Models | Overall recall | WEIRD | Serbian |
|---|---:|---:|---:|---:|
| Frontier/API | 5 | 0.615 | 0.590 | 0.641 |
| Open-weight | 6 | 0.578 | 0.590 | 0.565 |
| Small open-weight | 2 | 0.548 | 0.531 | 0.565 |
| All open-weight combined | 8 | 0.570 | 0.575 | 0.565 |

The API-minus-all-open difference is 0.045, or 4.5 percentage points. Its exact pair-blocked sign-flip test gives raw p = 0.086 and Holm-adjusted p = 0.258. The four-test family consists of the three pairwise category contrasts plus API versus all open-weight models. None meets 0.05 after correction; the smallest adjusted p is 0.063 (API versus Small open-weight). These are exploratory comparisons conditional on the selected models, not effects of openness or size.

`access_group_recall.csv` and `access_group_contrasts.csv` contain the revised category summaries and tests. `model_recall.csv` records both the original tier and the revised category. The original tier summaries and contrasts remain in `group_recall.csv` and `exploratory_contrasts.csv` for an audit trail, not as an alternative result selected for significance. Their previously observed Frontier–Small adjusted p = 0.023 applies to a different membership and must not be attached to the revised grouping.

The resampling confidence intervals and exact sign-flip tests are different finite-sample procedures; the percentile interval is not an inversion of the corrected test. Do not use an unadjusted interval to override an adjusted p-value.

## RQ3: two distinct comparisons

The country grouping is by developer identity: eight US models, four Chinese models, and one French model (Mistral). Mistral remains in RQ1 and RQ2 and is excluded only from the US–China contrast. This classification does not describe training-language composition or the nationality of a model's users.

| Developer group | Models | WEIRD recall | Serbian recall | Overall recall | WEIRD − Serbian |
|---|---:|---:|---:|---:|---:|
| US | 8 | 0.570 | 0.589 | 0.579 | −0.019 |
| China | 4 | 0.613 | 0.606 | 0.609 | +0.006 |

China's selected models have higher mean overall recall by 0.030, or 3.0 percentage points. The US-minus-China contrast has a new pair-bootstrap CI [−0.048, −0.013], exact two-sided pair-blocked sign-flip p = 0.023, and Holm-adjusted p = 0.047 across the two RQ3 outcomes. Their cultural-gap difference is −0.025 (CI [−0.082, 0.025]; p = 0.453, also 0.453 after correction). Higher overall recall and a different cultural gap are separate hypotheses.

These comparisons are conditional on the selected systems. The Chinese group contains one API and three larger open-weight models; the US group contains four API, two larger open-weight, and two smaller open-weight models, with multiple systems from some developers. Country is therefore confounded with model selection and category composition. Do not write that Chinese origin causes better recall or that these results establish a country-wide ranking.

## Changes elsewhere in the manuscript

- Change “two research questions” to “three”; label RQ2 and RQ3 exploratory if they were developed after the original analysis.
- Replace the F1-based ranking narrative with the recall-based table. Preserve the old precision/F1 table and definitions in an appendix, together with the distinction between unmatched output and invalid viewpoints.
- Update Table 2 to match the revised access categories, including the relocation of Qwen Max. Give access and relative size explicit definitions; do not treat frontier, open, and small as naturally disjoint concepts.
- Move the topic-variation discussion into RQ1 or place it immediately after that result.
- Keep judge checks as the last Results subsection. Agreement is evidence of consistency; it is not evidence that shared bias is absent.
- Remove causal or equivalence language such as “Serbian controversies do not incur an additional systematic penalty.” Use “we did not detect an additional recall disadvantage in these matched topics.”
- Describe the original mixed-effects result (p = 0.626) as the original **per-reference** analysis if retaining it. It is a different specification from the new **model-by-pair gap** analysis (p = 0.733). The old specification does not explicitly model all dependence among reference scores within a model-topic response. Do not replace one p-value with the other without replacing the methods text.
- Ensure the conclusion mentions RQ2 and RQ3 as exploratory, without letting a country comparison replace the primary cultural-coverage question.
- Continue to write “Serbian (non-WEIRD)” rather than implying that Serbia represents all non-WEIRD societies.

## Reproducibility and handoff

Run `.venv/bin/python paper/supervisor_revision/recalculate.py` from the repository root. The script validates all 208 topic scores against the original model means, reproduces the main exact p-value and historical bootstrap interval, and produces the new tables, matrix, sensitivity results, and figure. The historical interval uses a shared RNG after the original 78 model-comparison simulations; resetting seed 42 immediately before that bootstrap produces slightly different endpoints. New bootstraps use explicitly reset streams.

Authoritative inputs: `results/agg/prf_per_topic.csv`, `results/agg/ranking.csv`, `results/agg/weird_gap_summary.csv`, and `config/models.json`. The original recalled means and main inference were independently checked against the saved judgments. Pre-existing code edits in the workspace were left untouched.

Publication status: the replacement passages and numerical tables are ready for review. The category mapping is explicit, and source links explain why Qwen Max is in the API group. The remaining integration work is to copy the replacement passages into the current submission source and update its cross-references. No claim is made that the new exploratory contrasts were prespecified, that original citations have been audited, or that this pack replaces the complete submission source.
