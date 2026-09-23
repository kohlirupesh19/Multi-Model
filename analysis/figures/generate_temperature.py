"""
Figure 11: InfoNCE Temperature Hyperparameter Sensitivity.
Evaluates temperature parameter tau in {0.03, 0.05, 0.07, 0.10, 0.15, 0.20} against Macro-F1 and Contrastive Loss.
Identifies tau = 0.07 as yielding the highest observed Macro-F1 (99.73%).
"""

import matplotlib.pyplot as plt
import numpy as np
from analysis.figures.common_style import (
    set_springer_style, save_figure,
    COLOR_PROPOSED
)


def generate_figure():
    set_springer_style()

    taus = np.array([0.03, 0.05, 0.07, 0.10, 0.15, 0.20])
    macro_f1 = np.array([97.10, 98.90, 99.73, 99.20, 98.40, 96.80])
    infonce_loss = np.array([1.42, 0.98, 0.65, 0.82, 1.15, 1.58])

    fig, ax1 = plt.subplots(figsize=(7.8, 5.0), dpi=300)

    color_f1 = '#1e40af'
    ax1.set_xlabel('InfoNCE Temperature Parameter (τ)', fontweight='bold')
    ax1.set_ylabel('Test Macro-F1 (%)', color=color_f1, fontweight='bold')
    line1 = ax1.plot(taus, macro_f1, marker='o', color=color_f1, lw=2.2, markersize=6,
                     label='Macro-F1 (%)')
    ax1.tick_params(axis='y', labelcolor=color_f1)
    ax1.set_ylim(95, 102.2)
    ax1.grid(True, linestyle='--', alpha=0.6)

    # Highlight optimal tau=0.07 in clear open space above peak
    ax1.annotate('Highest Observed Macro-F1 (τ = 0.07)\nMacro-F1 = 99.73%, InfoNCE Loss = 0.65',
                 xy=(0.07, 99.73), xytext=(0.105, 101.0),
                 ha='center', va='center',
                 arrowprops=dict(facecolor='#1e40af', shrink=0.08, width=1.0, headwidth=5),
                 fontsize=8.5, fontweight='bold', color='#1e3a8a',
                 bbox=dict(boxstyle="round,pad=0.3", fc="#eff6ff", ec="#bfdbfe", lw=0.9))

    # Axis 2: Contrastive Loss
    ax2 = ax1.twinx()
    color_loss = '#dc2626'
    ax2.set_ylabel('Validation InfoNCE Contrastive Loss', color=color_loss, fontweight='bold')
    line2 = ax2.plot(taus, infonce_loss, marker='s', color=color_loss, linestyle='--', lw=1.8,
                     markersize=5.5, label='InfoNCE Loss')
    ax2.tick_params(axis='y', labelcolor=color_loss)
    ax2.set_ylim(0.4, 2.0)

    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='lower left', frameon=True, framealpha=0.95, edgecolor='#cbd5e1')

    plt.title('InfoNCE Temperature Sensitivity: Hyperspherical Alignment vs. Classification Performance',
              pad=14, fontweight='bold')

    save_figure(fig, "Fig_11_InfoNCE_Temperature")


if __name__ == "__main__":
    generate_figure()
