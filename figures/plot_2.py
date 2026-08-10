from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Resolve inputs/outputs next to this script so it runs from any cwd.
HERE = Path(__file__).resolve().parent


# 1. Load dataset
df_model = pd.read_csv(HERE / 'Per-model_WEIRD_coverage_gap.csv')

# Reverse dataframe order so top-ranked model displays at top of Y-axis
df_plot = df_model.iloc[::-1].reset_index(drop=True)

# Color scheme definitions
COLOR_BLUE = '#2b5ecb'
COLOR_BROWN = '#be621d'
COLOR_LIGHT_BLUE = '#8faadc'
COLOR_LIGHT_BROWN = '#e2b38b'

# Initialize figure
fig, ax = plt.subplots(figsize=(11, 7.5), dpi=300)

y_positions = np.arange(len(df_plot))

# 2. Plot stems and markers for individual models
for i, row in df_plot.iterrows():
    val = row['Mean gap']
    model_name = row['Model']
    if model_name == 'Gemma 4 31B':
        model_name = 'Gemma 4'

    color_dot = COLOR_BROWN if val > 0 else COLOR_BLUE
    color_line = COLOR_LIGHT_BROWN if val > 0 else COLOR_LIGHT_BLUE

    # Stem line from center 0 to mean gap value
    ax.plot([0, val], [i, i], color=color_line, linewidth=2, zorder=2)
    # End circle marker
    ax.scatter(val, i, color=color_dot, s=80, zorder=3)

# Set model y-axis labels
y_labels = [m if m != 'Gemma 4 31B' else 'Gemma 4' for m in df_plot['Model']]
ax.set_yticks(y_positions)
ax.set_yticklabels(y_labels, fontsize=11)

# 3. Center line and divider line
ax.axhline(y=-0.8, color='gray', linestyle='--', linewidth=1, alpha=0.7)
ax.axvline(x=0, color='gray', linestyle='-', linewidth=1, alpha=0.8)

# 4. Pooled diamond and 95% CI error bar
pooled_mean = -0.013
ci_lower = -0.081
ci_upper = 0.058
pooled_y = -2.2

# Horizontal bar and caps for CI
ax.plot([ci_lower, ci_upper], [pooled_y, pooled_y], color='black', linewidth=2.5, zorder=3)
ax.plot([ci_lower, ci_lower], [pooled_y - 0.2, pooled_y + 0.2], color='black', linewidth=2.5, zorder=3)
ax.plot([ci_upper, ci_upper], [pooled_y - 0.2, pooled_y + 0.2], color='black', linewidth=2.5, zorder=3)
ax.scatter(pooled_mean, pooled_y, color='black', marker='D', s=100, zorder=4)

# Text labels for pooled estimate
ax.text(0.063, pooled_y + 0.15, "pooled  −0.013", fontsize=10, va='bottom', color='black')
ax.text(0.063, pooled_y - 0.35, "95% CI  −0.081 to 0.058", fontsize=10, va='top', color='black')

# 5. Header annotations above x=0 axis line
ax.text(-0.02, 13.5, "covers Serbian arm more fully (n = 8)", color=COLOR_BLUE, fontsize=11, ha='right', va='center')
ax.text(0.02, 13.5, "covers WEIRD arm more fully (n = 5)", color=COLOR_BROWN, fontsize=11, ha='left', va='center')

# 6. Axes formatting
ax.set_title("The thirteen models split in sign; no gap survives correction", fontsize=13, loc='left', pad=25)
ax.set_xlabel("Mean coverage gap (WEIRD − Serbian)", fontsize=12, labelpad=10)

ax.set_xlim(-0.15, 0.20)
ax.set_ylim(-3.2, 14.2)
ax.set_xticks([-0.15, -0.10, -0.05, 0.00, 0.05, 0.10, 0.15, 0.20])

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_linewidth(1.2)
ax.tick_params(axis='y', length=0)

plt.tight_layout()
plt.savefig(HERE / 'per_model_coverage_gap.png', bbox_inches='tight')
plt.show()
