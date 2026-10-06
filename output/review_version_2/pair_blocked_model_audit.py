"""Audit saved recall scores, without model calls or changes to project files.

Run: /Users/vuk/Downloads/BWEIRD/.venv/bin/python /Users/vuk/Downloads/BWEIRD/output/review_version_2/pair_blocked_model_audit.py
"""
from itertools import product
from pathlib import Path
import json

import numpy as np
import pandas as pd
from statsmodels.stats.multitest import multipletests

ROOT = Path('/Users/vuk/Downloads/BWEIRD')
OUT = Path(__file__).resolve().parent
TOL = 1e-12


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
           'scope': 'Existing-score sensitivity; no generation/judgment experiments or data authentication.'}
(OUT / 'pair_blocked_model_audit_summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary, indent=2))
print(result.head(8).to_string(index=False))
