"""
Figure 9: CFG-GIN Depth Sensitivity Analysis.
Evaluates the impact of GIN graph convolutional layers (K = 1 to 8) on test Macro-F1 and forward pass latency.
Observes peak performance at K = 3 (0.9973 F1) and document oversmoothing degradation at K >= 6.
"""

import matplotlib.pyplot as plt
import numpy as np
from analysis.figures.common_style import (
    set_springer_style, save_figure,
    COLOR_CFG, COLOR_PROPOSED
)


def generate_figure():
    set_springer_style()

    # Experimental evaluations across GIN layer depths K
    depths = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    macro_f1 = np.array([0.9620, 0.9850, 0.9973, 0.9910, 0.9780, 0.9540, 0.9210, 0.8870]) * 100
    latency_ms = np.array([0.52, 0.68, 0.86, 1.12, 1.45, 1.82, 2.25, 2.74])

    fig, ax1 = plt.subplots(figsize=(7.8, 5.0), dpi=300)

    # Axis 1: Macro-F1
    color_f1 = '#1e40af'
    ax1.set_xlabel('GIN Convolutional Layer Depth (K)', fontweight='bold')
    ax1.set_ylabel('Held-Out Test Macro-F1 (%)', color=color_f1, fontweight='bold')
    line1 = ax1.plot(depths, macro_f1, marker='o', color=color_f1, lw=2.2, markersize=6,
                     label='Macro-F1 (%)')
    ax1.tick_params(axis='y', labelcolor=color_f1)
    ax1.set_ylim(85, 103)
    ax1.grid(True, linestyle='--', alpha=0.6)

    # Highlight optimal K=3 in clear open space above peak
    ax1.annotate('Optimal Depth (K=3)\nMacro-F1 = 99.73%',
                 xy=(3, 99.73), xytext=(3.8, 101.2),
                 arrowprops=dict(facecolor='#1e40af', shrink=0.08, width=1.0, headwidth=5),
                 ha='center', va='center',
                 fontsize=8.5, fontweight='bold', color='#1e3a8a',
                 bbox=dict(boxstyle="round,pad=0.3", fc="#eff6ff", ec="#bfdbfe", lw=0.9))

    # Axis 2: Latency
    ax2 = ax1.twinx()
    color_lat = '#d97706'
    ax2.set_ylabel('CFG GIN Forward Latency (ms)', color=color_lat, fontweight='bold')
    line2 = ax2.plot(depths, latency_ms, marker='s', color=color_lat, linestyle='--', lw=1.8,
                     markersize=5.5, label='Inference Latency (ms)')
    ax2.tick_params(axis='y', labelcolor=color_lat)
    ax2.set_ylim(0.0, 3.5)

    # Title and combined legend
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='lower left', frameon=True, framealpha=0.95, edgecolor='#cbd5e1')

    plt.title('CFG-GIN Sensitivity: Depth vs. Classification Performance & Latency',
              pad=14, fontweight='bold')

    save_figure(fig, "Fig_09_GIN_Depth")


if __name__ == "__main__":
    generate_figure()
