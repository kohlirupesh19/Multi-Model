"""
Figure 14: Generalization Protocols Comparison.
Compares Random Split (Test), Temporal Cutoff Split, and Family-Holdout Protocol.
Evaluates Accuracy, Macro-F1, Recall, and False Positive Rate across distinct evaluation methodologies.
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from analysis.figures.common_style import (
    set_springer_style, save_figure,
    TEST_EVAL_JSON, TEMPORAL_EVAL_JSON, FAMILY_EVAL_JSON
)


def generate_figure():
    set_springer_style()

    with open(TEST_EVAL_JSON, "r") as f:
        test_data = json.load(f)
    with open(TEMPORAL_EVAL_JSON, "r") as f:
        temporal_data = json.load(f)
    with open(FAMILY_EVAL_JSON, "r") as f:
        family_data = json.load(f)

    protocols = [
        ("Random Stratified\nHeld-Out Split", test_data["metrics"]),
        ("Temporal Cutoff Split\n(No Look-Ahead)", temporal_data["metrics"]),
        ("Sample-Level Family\nHoldout (WannaCry)", family_data["metrics"])
    ]

    names = [p[0] for p in protocols]
    accs = [p[1]["accuracy"] * 100 for p in protocols]
    f1s = [p[1]["f1_score"] * 100 for p in protocols]
    recs = [p[1]["recall"] * 100 for p in protocols]
    fprs = [p[1]["fpr"] * 100 for p in protocols]

    x = np.arange(len(names))
    width = 0.20

    fig, ax = plt.subplots(figsize=(8.8, 5.2), dpi=300)

    rects1 = ax.bar(x - 1.5 * width, accs, width, label='Accuracy (%)',
                    color='#1e40af', edgecolor='#172554', lw=0.9)
    rects2 = ax.bar(x - 0.5 * width, f1s, width, label='Macro-F1 (%)',
                    color='#7c3aed', edgecolor='#4c1d95', lw=0.9)
    rects3 = ax.bar(x + 0.5 * width, recs, width, label='Recall (%)',
                    color='#059669', edgecolor='#064e3b', lw=0.9)
    rects4 = ax.bar(x + 1.5 * width, fprs, width, label='False Positive Rate (%)',
                    color='#dc2626', edgecolor='#7f1d1d', lw=0.9)

    for r in [rects1, rects2, rects3]:
        for rect in r:
            h = rect.get_height()
            ax.annotate(f"{h:.2f}%", xy=(rect.get_x() + rect.get_width() / 2, h),
                        xytext=(0, 3), textcoords="offset points", ha='center', va='bottom',
                        fontsize=7.5, fontweight='bold', color='#1e293b')

    for rect in rects4:
        h = rect.get_height()
        ax.annotate(f"{h:.2f}%", xy=(rect.get_x() + rect.get_width() / 2, h),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom',
                    fontsize=7.5, fontweight='bold', color='#991b1b')

    ax.set_ylabel('Metric Rate / Score (%)', fontweight='bold')
    ax.set_title('Generalization Across Distinct Evaluation Protocols',
                 pad=24, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(names, fontsize=8.8, fontweight='bold')
    ax.set_ylim(0, 118)
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.08), frameon=True,
              framealpha=0.95, edgecolor='#cbd5e1', ncol=4, fontsize=8.5)

    save_figure(fig, "Fig_14_Generalization_Protocols")


if __name__ == "__main__":
    generate_figure()
