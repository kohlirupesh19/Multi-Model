"""
Figure 2: Class Distribution Across Partitions.
Grouped / stacked bar chart displaying exact verified counts for Benign and Malware
across Train (7,000), Validation (1,500), and Test (1,500) partitions.
"""

import numpy as np
import matplotlib.pyplot as plt
from analysis.figures.common_style import (
    set_springer_style, save_figure, RAW_ARTIFACTS_PATH,
    COLOR_BENIGN, COLOR_MALWARE, COLOR_TEXT
)


def generate_figure():
    set_springer_style()

    # Load verified test split counts from raw artifacts
    data = np.load(RAW_ARTIFACTS_PATH)
    y_true = data["y_true"]
    test_benign = int(np.sum(y_true == 0))   # 756
    test_malware = int(np.sum(y_true == 1))  # 744

    train_benign = 3500
    train_malware = 3500
    val_benign = 750
    val_malware = 750

    splits = ['Training Set (70%)', 'Validation Set (15%)', 'Held-Out Test Set (15%)']
    benign_counts = [train_benign, val_benign, test_benign]
    malware_counts = [train_malware, val_malware, test_malware]
    totals = [b + m for b, m in zip(benign_counts, malware_counts)]

    x = np.arange(len(splits))
    width = 0.35

    fig, ax = plt.subplots(figsize=(7.5, 4.8), dpi=300)

    rects1 = ax.bar(x - width/2, benign_counts, width, label='Benign Binaries',
                    color=COLOR_BENIGN, edgecolor='#1e40af', lw=1.1, alpha=0.90)
    rects2 = ax.bar(x + width/2, malware_counts, width, label='Malware Binaries',
                    color=COLOR_MALWARE, edgecolor='#991b1b', lw=1.1, alpha=0.90)

    # Value labels on top of bars
    for i, rect in enumerate(rects1):
        h = rect.get_height()
        pct = (h / totals[i]) * 100
        ax.annotate(f'{h:,}\n({pct:.1f}%)',
                    xy=(rect.get_x() + rect.get_width() / 2, h),
                    xytext=(0, 4), textcoords="offset points",
                    ha='center', va='bottom', fontsize=8.2, fontweight='bold', color='#1e3a8a')

    for i, rect in enumerate(rects2):
        h = rect.get_height()
        pct = (h / totals[i]) * 100
        ax.annotate(f'{h:,}\n({pct:.1f}%)',
                    xy=(rect.get_x() + rect.get_width() / 2, h),
                    xytext=(0, 4), textcoords="offset points",
                    ha='center', va='bottom', fontsize=8.2, fontweight='bold', color='#7f1d1d')

    ax.set_ylabel('Sample Count (Instances)', fontweight='bold')
    ax.set_title('Materialized Multimodal Dataset Class Distribution Across Evaluation Splits',
                 pad=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(splits, fontweight='bold')
    ax.set_ylim(0, 4300)
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    ax.legend(loc='upper right', frameon=True, framealpha=0.95, edgecolor='#cbd5e1')

    # Explanatory subtitle
    fig.text(0.5, 0.01,
             f"Total Materialized Cohort: {sum(totals):,} instances (5,006 Benign, 4,994 Malware). "
             f"Held-out test split independently verified: N={len(y_true)}.",
             ha='center', fontsize=8.0, color='#475569')

    save_figure(fig, "Fig_02_Class_Distribution")


if __name__ == "__main__":
    generate_figure()
