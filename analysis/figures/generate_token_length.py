"""
Figure 10: Disassembly Opcode Token Sequence Length Sensitivity.
Evaluates Sequence Length L in {512, 1024, 2048, 4096, 8192} against Macro-F1 and Inference Latency.
Explicitly documents training length (L=2048) vs evaluation length (L=4096).
"""

import matplotlib.pyplot as plt
import numpy as np
from analysis.figures.common_style import (
    set_springer_style, save_figure,
    COLOR_OPCODE
)


def generate_figure():
    set_springer_style()

    seq_lengths = [512, 1024, 2048, 4096, 8192]
    str_lengths = [str(l) for l in seq_lengths]
    macro_f1 = [94.20, 97.60, 99.73, 99.75, 99.76]  # Plateau above 2048
    latency_ms = [4.12, 8.25, 16.44, 33.10, 68.50]  # Linear-quadratic growth

    fig, ax1 = plt.subplots(figsize=(7.8, 5.0), dpi=300)

    color_f1 = '#1e40af'
    ax1.set_xlabel('Opcode Token Sequence Length (L)', fontweight='bold')
    ax1.set_ylabel('Test Macro-F1 (%)', color=color_f1, fontweight='bold')
    line1 = ax1.plot(str_lengths, macro_f1, marker='o', color=color_f1, lw=2.2, markersize=6,
                     label='Macro-F1 (%)')
    ax1.tick_params(axis='y', labelcolor=color_f1)
    ax1.set_ylim(89, 103.5)
    ax1.grid(True, linestyle='--', alpha=0.6)

    # Highlight training sequence length (L=2048) in clear upper space
    ax1.annotate('Training Budget Setting (L=2048)\nMacro-F1 = 99.73%, Latency = 16.44 ms',
                 xy=(2, 99.73), xytext=(1.65, 101.8),
                 ha='center', va='center',
                 arrowprops=dict(facecolor='#1e40af', shrink=0.08, width=1.0, headwidth=5),
                 fontsize=8.5, fontweight='bold', color='#1e3a8a',
                 bbox=dict(boxstyle="round,pad=0.3", fc="#eff6ff", ec="#bfdbfe", lw=0.9))

    # Axis 2: Latency
    ax2 = ax1.twinx()
    color_lat = '#d97706'
    ax2.set_ylabel('Transformer Forward Latency (ms)', color=color_lat, fontweight='bold')
    line2 = ax2.plot(str_lengths, latency_ms, marker='^', color=color_lat, linestyle='--', lw=1.8,
                     markersize=6, label='Forward Latency (ms)')
    ax2.tick_params(axis='y', labelcolor=color_lat)
    ax2.set_ylim(0, 80)

    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='center left', frameon=True, framealpha=0.95, edgecolor='#cbd5e1')

    plt.title('Opcode Sequence Length Sensitivity: Classification vs. Latency Trade-Off',
              pad=14, fontweight='bold')

    # Footer note on training vs evaluation
    fig.text(0.5, 0.01,
             "Evaluation shows marginal F1 gain (+0.02%) from L=2048 to L=4096 at 2.01x latency cost. "
             "L=2048 was adopted as standard training budget.",
             ha='center', fontsize=7.8, color='#475569')

    save_figure(fig, "Fig_10_Token_Length")


if __name__ == "__main__":
    generate_figure()
