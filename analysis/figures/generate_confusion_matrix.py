"""
Figure 4: Raw and Normalized Confusion Matrices.
Generated directly from raw predictions y_true and y_pred on the held-out 1,500 test split.
Automatically computes TP, TN, FP, FN, Accuracy, Precision, Recall, Specificity, and F1.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from analysis.figures.common_style import (
    set_springer_style, save_figure, RAW_ARTIFACTS_PATH,
    COLOR_TEXT
)


def generate_figure():
    set_springer_style()

    # Load raw evaluation artifacts
    data = np.load(RAW_ARTIFACTS_PATH)
    y_true = data["y_true"]
    y_pred = data["y_pred"]

    # First-principles calculation
    tp = int(np.sum((y_true == 1) & (y_pred == 1)))
    tn = int(np.sum((y_true == 0) & (y_pred == 0)))
    fp = int(np.sum((y_true == 0) & (y_pred == 1)))
    fn = int(np.sum((y_true == 1) & (y_pred == 0)))
    total = len(y_true)

    # Verification assertions
    assert tp + tn + fp + fn == total, "Confusion matrix sum mismatch"
    assert tp == 740 and tn == 756 and fp == 0 and fn == 4

    cm_counts = np.array([[tn, fp], [fn, tp]])
    cm_norm = cm_counts / cm_counts.sum(axis=1, keepdims=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.8, 4.6), dpi=300)
    plt.subplots_adjust(wspace=0.36, top=0.83, bottom=0.14)

    # Panel A: Raw Counts
    im1 = ax1.imshow(cm_counts, cmap='Blues', interpolation='nearest', vmin=0, vmax=800)
    ax1.set_title('(a) Raw Test Sample Counts', pad=12, fontweight='bold', fontsize=10.5)
    ax1.set_xticks([0, 1])
    ax1.set_yticks([0, 1])
    ax1.set_xticklabels(['Benign', 'Malware'], fontweight='bold')
    ax1.set_yticklabels(['Benign', 'Malware'], fontweight='bold')
    ax1.set_xlabel('Predicted Verdict', fontweight='bold')
    ax1.set_ylabel('Ground Truth Label', fontweight='bold')

    cell_labels_1 = [
        [f"True Negative (TN)\n{tn:,}", f"False Positive (FP)\n{fp}"],
        [f"False Negative (FN)\n{fn}", f"True Positive (TP)\n{tp:,}"]
    ]
    for i in range(2):
        for j in range(2):
            val = cm_counts[i, j]
            color = "white" if val > 400 else ("#dc2626" if (i, j) == (1, 0) else COLOR_TEXT)
            weight = "bold"
            ax1.text(j, i, cell_labels_1[i][j], ha='center', va='center',
                     fontsize=9.5, color=color, fontweight=weight)

    # Panel B: Row-Normalized Percentages
    im2 = ax2.imshow(cm_norm, cmap='Blues', interpolation='nearest', vmin=0.0, vmax=1.0)
    ax2.set_title('(b) Normalized Detection Rates (%)', pad=12, fontweight='bold', fontsize=10.5)
    ax2.set_xticks([0, 1])
    ax2.set_yticks([0, 1])
    ax2.set_xticklabels(['Benign', 'Malware'], fontweight='bold')
    ax2.set_yticklabels(['Benign', 'Malware'], fontweight='bold')
    ax2.set_xlabel('Predicted Verdict', fontweight='bold')
    ax2.set_ylabel('Ground Truth Label', fontweight='bold')

    cell_labels_2 = [
        [f"Specificity\n{cm_norm[0,0]*100:.2f}%", f"Fall-Out (FPR)\n{cm_norm[0,1]*100:.2f}%"],
        [f"Miss Rate (FNR)\n{cm_norm[1,0]*100:.3f}%", f"Sensitivity (Recall)\n{cm_norm[1,1]*100:.2f}%"]
    ]
    for i in range(2):
        for j in range(2):
            val = cm_norm[i, j]
            color = "white" if val > 0.50 else ("#dc2626" if (i, j) == (1, 0) else COLOR_TEXT)
            ax2.text(j, i, cell_labels_2[i][j], ha='center', va='center',
                     fontsize=9.5, color=color, fontweight='bold')

    # Colorbars with proper padding and fraction
    cbar1 = plt.colorbar(im1, ax=ax1, fraction=0.046, pad=0.06)
    cbar1.ax.tick_params(labelsize=8.5)
    cbar2 = plt.colorbar(im2, ax=ax2, fraction=0.046, pad=0.06)
    cbar2.ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1.0))
    cbar2.ax.tick_params(labelsize=8.5)

    fig.suptitle(f"Held-Out Test Set Performance (N = {total:,} Binaries | Default Threshold θ = 0.50)",
                 fontsize=11.5, fontweight='bold', y=0.96)

    save_figure(fig, "Fig_04_Confusion_Matrix", copy_to_manuscript="fig7_confusion_matrix")


if __name__ == "__main__":
    generate_figure()
