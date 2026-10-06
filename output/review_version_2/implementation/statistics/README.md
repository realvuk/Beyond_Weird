# Existing-data statistical sensitivity

Run from the BWEIRD repository root:

```sh
.venv/bin/python output/review_version_2/implementation/statistics/reproduce_sensitivity.py
```

The script reads saved model-topic recall scores. It makes no API calls, changes no manuscript or original result files, and writes only into this folder. The assertions in the script provide the runnable verification check.

## Results and interpretation

- **Pairwise model comparisons:** the original 16-topic Monte Carlo procedure has 15 BH-adjusted results below 0.05. Exact enumeration using the same 16 topic units also gives 15. Retaining the eight matched pairs as blocks yields 0, with minimum adjusted p = 0.08705357. The mean recall differences are unchanged. This demonstrates sensitivity to the inferential unit, not a proof that the original procedure is invalid. The manuscript should state the sign-exchangeability assumptions and present both analyses. It should not silently replace the original analysis or imply equivalence between models.
- **Model confidence intervals:** all original 16-topic percentile-bootstrap intervals independently reproduce from the saved scores within 1e-12. New eight-pair percentile intervals use 10,000 resamples and seed 42, retaining both cultural arms of each pair. They are wider for six models and narrower for seven. Pair blocking therefore does not uniformly widen intervals. These are topic-sampling sensitivities for fixed models, not repeated-generation uncertainty.
- **RQ3 overall recall:** the saved US-minus-China effect and interval independently reproduce: -0.03011719; 95% pair-bootstrap CI [-0.04843750, -0.01335937]; exact raw p = 0.0234375. The existing saved Holm-adjusted p is 0.046875. Add the effect interval to the main RQ3 result while retaining the existing fixed-model and confounding caveats.

## Assumptions and reporting corrections

The primary RQ1 analysis already states the correct eight-pair unit, averaging the 13 selected models within each pair. It explicitly states independence and symmetry for the signed-rank test and distinguishes its shift hypothesis from the arithmetic mean. It also acknowledges that the 104 model-pair observations are not independent. These statements should be preserved. The investigator-guided selection does not establish that the eight pairs are a probability sample or that the assumptions hold; no universal cultural conclusion follows.

The reported power values are for a noncentral-t calculation, not the primary signed-rank procedure. Label them as an illustrative one-sample t-test calculation under a normal location model with the observed SD. The t interval and upper bound are also conditional on that model. The old appendix phrase calling [-0.08096, 0.05823] the “reported primary interval” should instead say “pair-bootstrap interval,” since the main text foregrounds the t interval. These corrections retain the numbers.

`proposed_statistical_revisions.tex` provides exact replacement/insertion blocks for the editor. Its `supplementary/` paths assume the two CSV files below are copied into the final source package's supplementary folder.

## Artifacts and checks

- `pair_blocked_model_comparisons.csv`: all 78 original Monte Carlo p-values and BH values, exact 16-topic p-values and BH values, and exact eight-pair p-values and BH values.
- `model_recall_interval_sensitivity.csv`: all 13 means, original intervals, paired intervals, and interval widths.
- `sensitivity_summary.json`: formulas, resampling settings, counts, and RQ3 verification.
- `proposed_statistical_revisions.tex`: paste-ready passages that keep original procedures and report the sensitivity explicitly.

The exact sign-flip tests enumerate every sign pattern and count absolute null statistics at least as large as the observed absolute statistic, with 1e-12 tolerance. BH adjustment is applied jointly to all 78 p-values for each procedure; the implementation is cross-checked against `statsmodels`. Checks also verify 208 unique model-topic cells, 13 complete models by eight pairs, unchanged observed contrasts, reproduction of original topic intervals, reproduction of the saved RQ3 interval, and the expected 15/15/0 discovery counts. Original topic intervals use ascending topic IDs; topic and pair bootstrap streams are independently initialized at seed 42. The same index draws are used across models within each scheme.

This is an existing-score analysis rerun. It does not authenticate the underlying data, reproduce model generations or judge calls, or validate judge accuracy.
