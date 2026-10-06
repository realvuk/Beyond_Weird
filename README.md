# Beyond WEIRD

**Model Scale Does Not Close the Perspective Gap: Matched WEIRD and Serbian
Controversies Reveal Difficulty, Not Cultural Bias**

A reproducible evaluation pipeline that measures how well 13 LLMs generate the
sociopolitical perspectives that actually exist in a population, scored against
an externally grounded gold standard by a family-disjoint panel of 5 LLM judges,
with the WEIRD-vs-Serbian coverage gap estimated by matched-pairs statistics.

The paper is in [`paper/Final_Full_Paper.pdf`](paper/Final_Full_Paper.pdf).

## Quick start

Every number in the paper can be re-derived from the committed data. **No API
key and no network access are required** — the raw model outputs and judge
verdicts are in the repository.

```bash
make install
make verify
```

`make verify` runs three independent checks and takes about a minute:

| Check | What it proves |
|---|---|
| `verify/test_smoke.py` | The coverage rule, agreement coefficients and parsers behave as specified, against hand-derived expected values. |
| `verify/check_manuscript_numbers.py` | The committed CSVs still say what the manuscript says. |
| `verify/reverify.py` | A from-scratch re-derivation — importing none of the project's own code, in exact rational arithmetic — agrees with both the CSVs and the paper. |

To rebuild the result CSVs rather than just check them:

```bash
make analysis
```

`make help` lists every target.

To reproduce the charts from both manuscript versions, run `make figures`.
PDF and PNG exports go to `output/pdf/paper_figures/`; see
[`figures/README.md`](figures/README.md) for the figure-to-paper mapping,
individual commands, input files, and reproducibility checks.

## What the study does

```
                    config/models.json ── 13 generator models
                    data/topics.json ──── 16 topics, 8 matched WEIRD/Serbian pairs
                    data/gold_standard.json ─ 5 gold perspectives per topic
                              │
  ┌───────────────────────────┴────────────────────────────┐
  │ STAGES 1-2 — call the OpenRouter API, need a key,      │
  │ checkpointed and resumable                             │
  └────────────────────────────────────────────────────────┘
        pipeline/1_generate_perspectives.py
              13 models x 16 topics, temperature 0
              └─> data/outputs/generations.jsonl
        pipeline/2_judge_panel.py
              5 family-disjoint judges per generation,
              gold order randomised independently per judge execution
              └─> data/outputs/judgments.jsonl
                              │
  ┌───────────────────────────┴────────────────────────────┐
  │ STAGES 3-6 — pure computation, re-runnable at any time │
  └────────────────────────────────────────────────────────┘
        pipeline/adapter.py      harness output ──> eval contract
              └─> results/adapted/{verdicts.jsonl,topics.json,panels.json}
        pipeline/3_aggregate.py  per-judge credit ──> per-gold credit ──> coverage
              └─> results/agg/{cells,gold_credit,coverage_topic,validity}.csv
                    ├──────────────────────────┬─────────────────────────┐
        pipeline/4_eval_prf.py       pipeline/5_eval_reliability.py
              coverage/precision/F1        Fleiss kappa, Gwet AC1,
              + bootstrap CIs              Krippendorff alpha; judge kappas
              └─> ranking.csv,             └─> inter_judge_agreement.csv,
                  prf_per_topic.csv            pairwise_judge_{kappa,overlap}.csv
                    │
        pipeline/6_eval_stats.py  8 matched pairs, exact Wilcoxon signed-rank,
              rank-biserial, BH-corrected pairwise permutation tests,
              mixed-effects robustness model
              └─> results/agg/{pairwise_models,weird_gap_*,mixed_model}.csv
```

## Repository layout

```
bweird/           The library. analysis.py is the live analysis core: stages
                  3-6 import it and every number in results/agg/ comes from
                  it. The rest (schemas, config, openrouter, checkpoint,
                  parsing, prompts) serves the two API stages.
pipeline/         The six numbered stages plus adapter.py, in run order.
verify/           Three independent checks. Start here.
reanalysis/       A standalone re-implementation of the analysis, written
                  against the raw files from a different angle as a
                  corroboration. Two manuscript tables come only from here:
                  Table 5 and the leave-one-judge-out audit. Has its own
                  README.
annotation/       The human-annotation workflow: build the blind sheet (7),
                  backfill perspective text (10), adjudicate the completed
                  sheet (9).
figures/          The two manuscript figures and the scripts that draw them.
config/           models.json (13 generators), judges.json (5-judge base
                  panel + substitution dictionary). Family labels must agree
                  across both files.
data/             topics.json, gold_standard.json, and outputs/ — the raw
                  generations and judge verdicts, committed so the analysis
                  reproduces without API spend.
results/          agg/ (authoritative), adapted/, annotation/, reanalysis/,
                  verification/.
paper/            The manuscript.
```

## Method, and where each guarantee lives in the code

- **Temperature zero everywhere.** `OpenRouterClient.chat` defaults to
  `temperature=0.0`, both stages pass it explicitly, and a fixed provider-side
  `seed` is sent (`bweird/openrouter.py`).
- **Family-disjoint judging.** Any base judge sharing the generator's family is
  dropped and a pre-designated neutral substitute seated (`config/judges.json`;
  `bweird.analysis.resolve_panel` at analysis time). Panel size stays exactly 5,
  with no duplicate judges and no same-family seat. Both substitutes come from
  families absent from the base panel, so substitution cannot reintroduce a
  same-family pairing.
- **Independent presentation randomisation.** `2_judge_panel.presentation_rng`
  derives a fresh shuffle of the gold options for *every single judge execution*
  by hashing the run seed with the execution key: independent across executions,
  yet reproducible and resume-safe. Votes are mapped back from presented labels
  to canonical gold IDs before storage.
- **Soft aggregation, no majority threshold.** Coverage is aggregated from the
  panel's soft verdicts, never a hard majority label. Abstentions and API
  failures shrink the denominator; only valid votes count.
- **The credit-sum coverage rule** (`bweird.analysis.aggregate_model_topic`).
  Each judge's credit for a gold is split equally across however many of a
  topic's generations that judge matched to it. A generation's weight toward a
  gold is the mean of that per-judge credit over the judges that rated it. A
  gold's credit for a model is the sum of those weights across the topic's five
  generations. That sum is by construction the share of judges who found the
  gold expressed by *any* generation, so it cannot exceed 1 and no cap is
  applied. Per-topic coverage is the mean over the topic's 5 golds; model
  coverage is the mean over the 16 topics. Pass `--gold-credit max` to stages 4
  and 6 for the stricter single-best-generation variant.
- **Recall / precision / F1.** `4_eval_prf.py`: coverage (recall) as above;
  precision is the share of valid judges matching a generation to *any* gold;
  F1 is the harmonic mean of model-level coverage and precision.
- **Kappa-paradox-aware reliability.** `5_eval_reliability.py` reports Fleiss'
  kappa, Gwet's AC1 and Krippendorff's alpha side by side, pooled and per arm,
  with the no-match marginal share as the skew diagnostic. Pairwise Cohen's
  kappa between judges is reported alongside.
- **Within-family bias is precluded, not measured.** No judge ever scores a
  generator from its own family, so there is no within-family inflation to
  estimate and subtract. `5_eval_reliability.bias_control()` would measure it,
  but only from same-family verdicts collected via
  `2_judge_panel.py --include-family-probe`. Those were not collected for this
  study, and the function refuses to run rather than silently compare 4 judges
  against 5. There is no `results/family_bias.csv`.
- **Exact matched-pairs test.** `6_eval_stats.py` computes
  delta = coverage(WEIRD) − coverage(Serbian) per pair and runs an exact
  Wilcoxon signed-rank test via SciPy's `method="exact"` (full sign-permutation
  enumeration over the signed ranks), the rank-biserial effect size, and a
  percentile bootstrap CI, per model and pooled. Pairwise model comparisons use
  10,000-iteration paired permutation tests with Benjamini–Hochberg correction
  across all 78 pairs.

## Checkpointing and failure semantics

- JSONL checkpoints are append-only with flush+fsync per record. A truncated
  final line from a crash is skipped with a warning and its unit redone.
- **Stage 1**: permanently failed cells go to
  `data/outputs/generation_failures.jsonl` and are retried on the next run
  (exit code 1 signals incomplete coverage).
- **Stage 2**: a judge that fails after all retries is recorded as an
  **abstention** (`match = null`) — the seat stays in the data and downstream
  denominators adjust. `--retry-abstentions` re-runs those executions and
  **appends** a fresh record rather than overwriting; the newest record per key
  supersedes older ones downstream. This is why the study's 5,228 raw verdicts
  contain 28 duplicate tuples that resolve to 5,184 valid verdicts.

## Re-running the API stages

Only needed if you want to regenerate the raw data rather than analyse the
committed copy. This costs real money.

```bash
cp .env.example .env        # then paste your OpenRouter key into .env
python pipeline/1_generate_perspectives.py
python pipeline/2_judge_panel.py
python pipeline/2_judge_panel.py --retry-abstentions   # optional second pass
```

Both stages take `--dry-run` to list pending work without spending tokens, and
`--help` documents the rest. `.env` is git-ignored; an exported
`OPENROUTER_API_KEY` takes precedence over the file.

## Known discrepancy

`verify/reverify.py` reports **97 of 98 checks passing**. The one failure is
real and is a manuscript error, not a code error: section 4.5 attributes a
coverage of 0.644 to the Polish Catholic Church topic, where the data give
0.6154. The corrected value is written to
`results/verification/table6_corrected.csv`. The check is left failing on
purpose rather than adjusted to match the prose.

## Input files you would need to author for a new study

- **`data/topics.json`** — the instrument. Enforced at load time: unique
  `topic_id`s; every `pair_id` appears exactly twice, once with `"arm": "weird"`
  and once with `"arm": "serbian"`.
- **`data/gold_standard.json`** — exactly 5 externally grounded gold
  perspectives per topic, each with a canonical `perspective_id` and non-empty
  `summary`/`explanation`. Perspectives also carry an `extremity_tier` (1–3);
  it is metadata only and no pipeline stage reads it.
- **`config/models.json` / `config/judges.json`** — OpenRouter slugs. Family
  labels must be consistent across both files; the disjointness constraint
  operates on those labels.

## Development

```bash
make lint     # ruff + mypy
```

Strict typing covers the library's harness modules and the two API stages.
The numbered analysis stages, `bweird/analysis.py` and `reanalysis/` are
unannotated pandas code and are deliberately outside that scope; the
boundary is set in `pyproject.toml`.

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

## Citation

See `paper/Final_Full_Paper.pdf`. Licensed under the MIT License — set the
copyright holder in `LICENSE` before publishing.
