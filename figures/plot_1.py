from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# Resolve inputs/outputs next to this script so it runs from any cwd.
HERE = Path(__file__).resolve().parent


# 1. Load dataset
df = pd.read_csv(HERE / 'Mean_coverage_by_topic.csv')

# Separate pair rows from the summary mean row
pairs_df = df.iloc[0:8].copy()
mean_row = df.iloc[8]

# Formatted short pair labels matching the reference chart
short_labels = [
    "Confederate monuments / Partisans  (+0.1)",
    "Catalonia / Kosovo  (+5.5)",
    "UK fracking / Jadar  (+0.3)",
    "Polish Church / Serbian Church  (−2.9)",
    "Residential schools / Srebrenica  (−16.9)",
    "Germany immigration / Balkan route  (+19.1)",
    "Orbán / Vučić  (−10.1)",
    "Brexit / West-vs-Russia  (−5.6)"
]
pairs_df['Label'] = short_labels

# Color palette definitions
COLOR_BLUE = '#3b62d1'   # Favours Serbian topic
COLOR_BROWN = '#b85d19'  # Favours WEIRD topic

# Initialize figure
fig, ax = plt.subplots(figsize=(11, 6.5), dpi=300)

# 2. Plot slope lines for each pair
for _idx, row in pairs_df.iterrows():
    w_cov = row['Cov.']
    s_cov = row['Cov..1']
    delta_val = float(str(row['Δ (pp)']).replace('−', '-'))
    color = COLOR_BROWN if delta_val > 0 else COLOR_BLUE

    ax.plot([0, 1], [w_cov, s_cov], color=color, linewidth=2, marker='o', markersize=7)

# 3. Plot overall arm mean line (thick black line with square markers)
ax.plot([0, 1], [mean_row['Cov.'], mean_row['Cov..1']], color='black', linewidth=3.5, marker='s', markersize=8)
ax.text(-0.06, mean_row['Cov.'], 'arm mean', ha='right', va='center', fontsize=10, color='black')

# 4. Right-side labels with stepped leader lines
sorted_pairs = pairs_df.sort_values(by='Cov..1', ascending=False).reset_index(drop=True)
label_y_positions = [0.698, 0.679, 0.660, 0.641, 0.622, 0.603, 0.468, 0.449]

for i, row in sorted_pairs.iterrows():
    s_cov = row['Cov..1']
    target_y = label_y_positions[i]
    delta_val = float(str(row['Δ (pp)']).replace('−', '-'))
    color = COLOR_BROWN if delta_val > 0 else COLOR_BLUE

    # Stepped leader line: horizontal -> vertical step -> label anchor
    ax.plot([1.0, 1.03, 1.03, 1.08], [s_cov, s_cov, target_y, target_y], color=color, linewidth=0.8)
    ax.text(1.10, target_y, row['Label'], color=color, va='center', fontsize=10)

# 5. Axes formatting & limits
ax.set_xlim(-0.2, 1.8)
ax.set_ylim(0.435, 0.715)

ax.set_xticks([0, 1])
ax.set_xticklabels([
    f"WEIRD topic\n(mean {mean_row['Cov.']:.3f})",
    f"Serbian topic\n(mean {mean_row['Cov..1']:.3f})"
], fontsize=10)

ax.set_ylabel("Mean coverage across the thirteen models", fontsize=11, labelpad=10)
ax.set_title("Pair differences cross rather than align: four pairs favour each arm", fontsize=13, loc='left', pad=15)

# Minimalist spine configuration
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(1.2)
ax.spines['bottom'].set_linewidth(1.2)

plt.tight_layout()
plt.savefig(HERE / 'coverage_by_topic_slopechart.png', bbox_inches='tight')
plt.show()
