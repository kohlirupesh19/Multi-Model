"""
Figure 12: UPX Packing Robustness Evaluation.
Compares Clean Unpacked vs. UPX-Packed Binaries across Accuracy, F1, FPR, and FNR.
Strictly verifies reported degradation: Accuracy drops from 100.0% to 88.00%, FPR increases to 24.00% (0.24).
Reads directly from results/robustness_results.json.
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from analysis.figures.common_style import (
    set_springer_style, save_figure, ROBUSTNESS_JSON,
    COLOR_BENIGN, COLOR_MALWARE, COLOR_PROPOSED
)


def generate_figure():
    set_springer_style()

    with open(ROBUSTNESS_JSON, "r") as f:
        rob_data = json.load(f)

    clean = rob_data["clean"]
    upx = rob_data["upx_packing"]

    # Verify metrics
    assert abs(clean["accuracy"] - 1.0) < 1e-4
    assert abs(upx["accuracy"] - 0.88) < 1e-4
    assert abs(upx["f1_score"] - 0.8929) < 1e-4
    assert abs(upx["fpr"] - 0.24) < 1e-4
    assert abs(upx["fnr"] - 0.0) < 1e-4

    metrics = ['Detection Accuracy', 'Macro-F1 Score', 'False Positive Rate\n(Benign Fall-Out)', 'False Negative Rate\n(Malware Miss Rate)']
    clean_vals = [clean["accuracy"] * 100, clean["f1_score"] * 100, clean["fpr"] * 100, clean["fnr"] * 100]
    upx_vals = [upx["accuracy"] * 100, upx["f1_score"] * 100, upx["fpr"] * 100, upx["fnr"] * 100]

    x = np.arange(len(metrics))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8.8, 5.2), dpi=300)

    rects1 = ax.bar(x - width/2, clean_vals, width, label='Clean / Unpacked Binaries',
                    color='#059669', edgecolor='#064e3b', lw=1.0)
    rects2 = ax.bar(x + width/2, upx_vals, width, label='UPX-Packed Binaries (Evasion Test)',
                    color='#dc2626', edgecolor='#7f1d1d', lw=1.0)

    # Add data labels
    for rect in rects1:
        h = rect.get_height()
        ax.annotate(f"{h:.1f}%",
                    xy=(rect.get_x() + rect.get_width() / 2, h),
                    xytext=(0, 4), textcoords="offset points",
                    ha='center', va='bottom', fontsize=8.8, fontweight='bold', color='#065f46')

    for rect in rects2:
        h = rect.get_height()
        ax.annotate(f"{h:.1f}%",
                    xy=(rect.get_x() + rect.get_width() / 2, h),
                    xytext=(0, 4), textcoords="offset points",
                    ha='center', va='bottom', fontsize=8.8, fontweight='bold', color='#991b1b')

    # Explanatory callout for 24% FPR (positioned in empty space above Tick 3, pointing to side of bar)
    ax.annotate('Benign False Alarm Surge:\nFPR rises to 24.0% under UPX compression',
                xy=(x[2] + width, 14.0), xytext=(2.65, 52.0),
                arrowprops=dict(facecolor='#dc2626', shrink=0.08, width=1.0, headwidth=5),
                ha='center', va='center',
                fontsize=8.0, fontweight='bold', color='#991b1b',
                bbox=dict(boxstyle="round,pad=0.35", fc="#fef2f2", ec="#fca5a5", lw=0.9))

    ax.set_ylabel('Rate / Metric Value (%)', fontweight='bold')
    ax.set_title('UPX Obfuscation Impact: Performance Degradation & False Positive Spike',
                 pad=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontweight='bold')
    ax.set_ylim(0, 115)
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    ax.legend(loc='upper right', frameon=True, framealpha=0.95, edgecolor='#cbd5e1')

    fig.text(0.5, 0.01,
             "Verified from results/robustness_results.json. Malware detection remains 100.0% (FNR=0.0%), "
             "but benign misclassification triggers 24.0% false alarms.",
             ha='center', fontsize=7.8, color='#475569')

    save_figure(fig, "Fig_12_UPX_Robustness")


if __name__ == "__main__":
    generate_figure()
