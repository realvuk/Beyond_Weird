"""Small regression check: published values, order independence and invalid inputs."""

import shutil
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
from reproduce import ROOT, SOURCES, load_results, plot_pair_gaps, plt


def main():
    names, w, s, pooled, _ = load_results()
    assert len(names) == 13 and w.shape == s.shape == (13, 8)
    # Compare to the three-decimal values printed in the paper.
    np.testing.assert_allclose([w.mean(), s.mean(), pooled.mean_gap],
                               [.581, .594, -.013], rtol=0, atol=.0005)
    assert ((w - s).mean(axis=0) > 0).sum() == 4
    assert ((w - s).mean(axis=1) > 0).sum() == 5
    fig = plot_pair_gaps(names, w, s, pooled, None)
    interval = fig.axes[0].containers[0].lines[2][0].get_segments()[0]
    np.testing.assert_allclose(interval[:, 0], [-10.2918289999674, 7.676444384582787],
                               rtol=0, atol=1e-10)
    assert "95% t-based interval" in fig.texts[-1].get_text()
    plt.close(fig)
    with tempfile.TemporaryDirectory(prefix="bweird-chart-check-") as temp:
        root = Path(temp)
        for source in SOURCES:
            dest = root / source
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / source, dest)
        path = root / "results/agg/prf_per_topic.csv"
        cells = pd.read_csv(path)
        cells.sample(frac=1, random_state=42).to_csv(path, index=False)
        shuffled = load_results(root)
        np.testing.assert_allclose(shuffled[1], w)
        np.testing.assert_allclose(shuffled[2], s)
        for broken in [cells.iloc[:-1], pd.concat([cells, cells.iloc[:1]]),
                       cells.assign(coverage_sum=np.nan)]:
            broken.to_csv(path, index=False)
            try:
                load_results(root)
            except (ValueError, AssertionError):
                pass
            else:
                raise AssertionError("Invalid model-topic data was accepted.")
        cells.to_csv(path, index=False)
        summary_path = root / "results/agg/weird_gap_summary.csv"
        summary = pd.read_csv(summary_path)
        summary.loc[summary.analysis.eq("pooled_coverage"), "mean_ci_lo"] += .01
        summary.to_csv(summary_path, index=False)
        try:
            load_results(root)
        except AssertionError:
            pass
        else:
            raise AssertionError("An incorrect pooled confidence interval was accepted.")
    print("PASS: paper values, plotted t-interval, shuffled row order, missing/duplicate/NaN cells, and incorrect CI.")


if __name__ == "__main__":
    main()
