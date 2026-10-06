"""Reproduce supplementary sensitivities from saved model-topic recall scores.

Run from the repository root:
.venv/bin/python output/review_version_2/implementation/statistics/reproduce_sensitivity.py
Writes only to this script's folder; does not call models or alter saved inputs.
"""
from itertools import product
from pathlib import Path
import json

import numpy as np
import pandas as pd
from statsmodels.stats.multitest import multipletests

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
TOL = 1e-12
N_BOOT, SEED = 10_000, 42


def bh(p):
    p = np.asarray(p)
    order = np.argsort(p)
    adjusted = np.empty(len(p))
    adjusted[order] = np.minimum(1, np.minimum.accumulate(
        (p[order] * len(p) / np.arange(1, len(p) + 1))[::-1])[::-1])
    assert np.allclose(adjusted, multipletests(p, method='fdr_bh')[1], atol=TOL)
    return adjusted


data = pd.read_csv(ROOT / 'results/agg/prf_per_topic.csv')
assert len(data) == 208 and not data.duplicated(['generator', 'topic_id']).any()
data['pair'] = data.topic_id.str.extract(r'pair(\d+)').astype(int)
data['arm'] = data.topic_id.str.split('_').str[-1]
wide = data.pivot(index='generator', columns=['arm', 'pair'], values='coverage_sum')
W, S = wide.weird.to_numpy(), wide.serbian.to_numpy()
assert W.shape == S.shape == (13, 8) and np.isfinite(W + S).all()
pair_average = (W + S) / 2
both_topics = np.column_stack((W, S))
signs8 = np.asarray(list(product([-1, 1], repeat=8)))
signs16 = np.asarray(list(product([-1, 1], repeat=16)))


def exact_p(d, signs):
    statistic = d.mean()
    null = signs @ d / len(d)
    return float((np.abs(null) >= abs(statistic) - TOL).mean())


assert exact_p(np.arange(1, 9), signs8) == 2 / 256
assert exact_p(np.zeros(8), signs8) == 1
original = pd.read_csv(ROOT / 'results/agg/pairwise_models.csv')
assert len(original) == 78
rows = []
for row in original.itertuples(index=False):
    a, b = wide.index.get_loc(row.model_a), wide.index.get_loc(row.model_b)
    contrast = pair_average[a] - pair_average[b]
    assert abs(contrast.mean() - row.mean_coverage_diff) < TOL
    rows.append({'model_a': row.model_a, 'model_b': row.model_b,
                 'mean_recall_difference': contrast.mean(),
                 'original_16topic_mc_p': row.p_raw,
                 'original_16topic_mc_bh': row.p_bh,
                 'exact_16topic_p': exact_p(both_topics[a] - both_topics[b], signs16),
                 'pair_blocked_p': exact_p(contrast, signs8)})
result = pd.DataFrame(rows)
result['exact_16topic_bh'] = bh(result.exact_16topic_p)
result['pair_blocked_bh'] = bh(result.pair_blocked_p)
result.to_csv(OUT / 'pair_blocked_model_comparisons.csv', index=False)

# Identical pair-index draws across models retain both cultural arms of a pair.
# Original topic intervals are independently reproduced in canonical topic order.
pair_indices = np.random.default_rng(SEED).integers(0, 8, (N_BOOT, 8))
topic_indices = np.random.default_rng(SEED).integers(0, 16, (N_BOOT, 16))
ranking = pd.read_csv(ROOT / 'results/agg/ranking.csv').set_index('generator')
models = json.loads((ROOT / 'config/models.json').read_text())
names = {m['slug']: m['display_name'].replace(' Preview', '') for m in models}
intervals = []
for i, generator in enumerate(wide.index):
    values = data[data.generator == generator].sort_values('topic_id').coverage_sum.to_numpy()
    topic_ci = np.percentile(values[topic_indices].mean(axis=1), [2.5, 97.5])
    saved_ci = ranking.loc[generator, ['coverage_lo', 'coverage_hi']].to_numpy(float)
    assert np.allclose(topic_ci, saved_ci, rtol=0, atol=TOL)
    assert abs(pair_average[i].mean() - ranking.loc[generator, 'coverage']) < TOL
    pair_ci = np.percentile(pair_average[i][pair_indices].mean(axis=1), [2.5, 97.5])
    intervals.append({'model': names[generator], 'generator': generator,
                      'overall_recall': pair_average[i].mean(),
                      'original_16topic_ci_lo': topic_ci[0],
                      'original_16topic_ci_hi': topic_ci[1],
                      'pair_bootstrap_ci_lo': pair_ci[0],
                      'pair_bootstrap_ci_hi': pair_ci[1],
                      'original_interval_width': topic_ci[1] - topic_ci[0],
                      'pair_interval_width': pair_ci[1] - pair_ci[0]})
intervals = pd.DataFrame(intervals).sort_values('overall_recall', ascending=False)
intervals.to_csv(OUT / 'model_recall_interval_sensitivity.csv', index=False)

# Verify the saved RQ3 overall-recall effect interval, retaining selected models.
families = {m['slug']: m['family'] for m in models}
chinese = {'deepseek', 'alibaba', 'moonshot', 'z.ai'}
cn = [i for i, g in enumerate(wide.index) if families[g] in chinese]
us = [i for i, g in enumerate(wide.index) if families[g] not in chinese | {'mistral'}]
assert len(us) == 8 and len(cn) == 4
country_contrast = pair_average[us].mean(axis=0) - pair_average[cn].mean(axis=0)
country_ci = np.percentile(country_contrast[pair_indices].mean(axis=1), [2.5, 97.5])
country_saved = pd.read_csv(ROOT / 'output/pdf/version_3/supplementary/developer_country_contrasts.csv').iloc[0]
assert np.allclose([country_contrast.mean(), *country_ci],
                   country_saved[['recall_difference', 'recall_ci_lo', 'recall_ci_hi']].to_numpy(float),
                   rtol=0, atol=TOL)
assert exact_p(country_contrast, signs8) == country_saved.recall_p_two_sided
summary = {'inputs': ['results/agg/prf_per_topic.csv', 'results/agg/pairwise_models.csv'],
           'contrast': 'x_p = (R_a,W,p + R_a,S,p)/2 - (R_b,W,p + R_b,S,p)/2',
           'statistic': 'mean(x_p), retaining the original mean recall difference',
           'pair_null': 'all 256 sign vectors over 8 matched-pair contrasts',
           'two_sided_tail': 'mean(abs(null_statistic) >= abs(observed_statistic) - 1e-12)',
           'correction': 'Benjamini-Hochberg jointly over 78 tests, alpha=0.05',
           'original_mc_significant': int((result.original_16topic_mc_bh < .05).sum()),
           'exact_16topic_significant': int((result.exact_16topic_bh < .05).sum()),
           'pair_blocked_significant': int((result.pair_blocked_bh < .05).sum()),
           'pair_blocked_min_raw_p': float(result.pair_blocked_p.min()),
           'pair_blocked_min_bh_p': float(result.pair_blocked_bh.min()),
           'model_interval_sensitivity': {
               'n_resamples': N_BOOT, 'seed': SEED, 'method': 'percentile 2.5 and 97.5',
               'resampling_unit': '8 matched pairs, retaining both arms and fixed selected models',
               'point_estimates': 'unchanged; mean of 8 pair averages equals mean of 16 topics',
               'original_16topic_intervals': 'reproduced and matched results/agg/ranking.csv within 1e-12',
               'original_topic_order': 'ascending topic_id; shared seed42 draws independently initialized for topic and pair schemes',
               'paired_intervals_wider_count': int((intervals.pair_interval_width > intervals.original_interval_width + TOL).sum()),
               'paired_intervals_narrower_count': int((intervals.pair_interval_width < intervals.original_interval_width - TOL).sum())},
           'rq3_overall_recall': {
               'contrast': 'US minus China', 'n_us_models': len(us), 'n_chinese_models': len(cn),
               'difference': float(country_contrast.mean()), 'pair_bootstrap_ci': country_ci.tolist(),
               'raw_p': float(country_saved.recall_p_two_sided), 'holm_p': float(country_saved.recall_p_holm),
               'verification': 'effect, pair-bootstrap interval, and raw sign-flip p independently reproduce saved table'},
           'scope': 'Existing-score sensitivity; no generation/judgment experiments or data authentication.'}
assert (summary['original_mc_significant'], summary['exact_16topic_significant'], summary['pair_blocked_significant']) == (15, 15, 0)
(OUT / 'sensitivity_summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary, indent=2))
print(intervals[['model', 'overall_recall', 'original_16topic_ci_lo', 'original_16topic_ci_hi',
                 'pair_bootstrap_ci_lo', 'pair_bootstrap_ci_hi']].to_string(index=False))
