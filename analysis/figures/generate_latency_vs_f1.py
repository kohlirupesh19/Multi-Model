"""
Figure 17: Latency vs. Macro-F1 Pareto Analysis.
Scatter plot displaying Neural Forward Latency (ms) on X-axis vs. Test Macro-F1 (%) on Y-axis.
Compares verified models objectively without promotional bias.
Reads from FINAL_RESULTS.csv.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from analysis.figures.common_style import (
    set_springer_style, save_figure, FINAL_RESULTS_CSV
)


def generate_figure():
    set_springer_style()

    df = pd.read_csv(FINAL_RESULTS_CSV)

    models_to_plot = [
        ("Proposed Multi-Modal\n(Full Tri-Modal)", "EXP-01-PROPOSED-TEST", '#1d4ed8', 'o', 80),
        ("Fast Static Triage\n(Opcode + CFG)", "EXP-05-STATIC-TRIAGE", '#2563eb', 's', 70),
        ("Static Only (w/o Syscall)", "EXP-14-ABL-NO-SYSCALL", '#0284c7', '^', 65),
        ("w/o GRAM (InfoNCE Only)", "EXP-11-ABL-NO-GRAM", '#7c3aed', 'v', 65),
        ("w/o InfoNCE (GRAM Only)", "EXP-15-ABL-NO-INFONCE", '#9333ea', '<', 65),
        ("Early Concat MLP", "EXP-22-BASELINE-CONCAT", '#0891b2', 'D', 65),
        ("Opcode Transformer Only", "EXP-16-BASELINE-OPCODE", '#a855f7', 'p', 60),
        ("CFG GIN Only", "EXP-17-BASELINE-CFG", '#059669', 'h', 60),
        ("Syscall Bi-LSTM Only", "EXP-18-BASELINE-SYSCALL", '#d97706', '8', 60),
        ("MalConv (Raff et al. 2020)", "EXP-19-BASELINE-MALCONV", '#64748b', 'X', 60),
        ("Asm2Vec (Ding et al. 2019)", "EXP-21-BASELINE-ASM2VEC", '#475569', 'P', 60),
        ("Gemini (Xu et al. 2017)", "EXP-20-BASELINE-GEMINI", '#334155', '*', 75)
    ]

    fig, ax = plt.subplots(figsize=(9.4, 5.8), dpi=300)

    # Shaded efficient envelope (latency 15-30ms, F1 > 97.5%)
    # In data coords, y from 97.8 to 102.5
    y_min_plot, y_max_plot = 76.0, 102.8
    env_ymin_frac = (97.8 - y_min_plot) / (y_max_plot - y_min_plot)
    ax.axvspan(15, 30.5, ymin=env_ymin_frac, ymax=1.0, color='#eff6ff', alpha=0.7, zorder=1)
    ax.text(23.2, 98.2, "High-F1 Operating Envelope\n(F1 > 98%, Latency < 30ms)",
            ha='center', va='bottom', fontsize=7.8, fontstyle='italic', color='#1e3a8a',
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#ffffff', edgecolor='#bfdbfe', alpha=0.95),
            zorder=2)

    for name, exp_id, color, marker, size in models_to_plot:
        row = df[df["experiment_id"] == exp_id]
        if len(row) > 0:
            lat = row["latency_ms"].values[0]
            f1 = row["F1"].values[0] * 100
            ax.scatter(lat, f1, color=color, marker=marker, s=size, edgecolors='#1e293b',
                       lw=0.8, label=name.replace('\n', ' '), zorder=4)

    # Selective Pareto-frontier and landmark annotations with clean callout arrows
    annotations = [
        ("Proposed Multi-Modal\n(99.73%, 28.9 ms)", (28.87, 99.73), (22.8, 101.4), '#1d4ed8', 'right'),
        ("Fast Static Triage\n(99.23%, 17.5 ms)", (17.53, 99.23), (11.2, 100.4), '#2563eb', 'right'),
        ("CFG GIN Only\n(84.00%, 0.9 ms)", (0.86, 84.00), (3.8, 81.2), '#059669', 'left'),
        ("Syscall Bi-LSTM\n(79.84%, 11.1 ms)", (11.05, 79.84), (13.5, 78.2), '#d97706', 'left'),
    ]

    for label_text, xy, xytext, text_color, ha in annotations:
        ax.annotate(
            label_text,
            xy=xy,
            xytext=xytext,
            ha=ha,
            va='center',
            fontsize=7.8,
            fontweight='bold',
            color=text_color,
            arrowprops=dict(
                arrowstyle='->',
                color=text_color,
                lw=0.9,
                shrinkA=3,
                shrinkB=4,
                connectionstyle="arc3,rad=0.1"
            ),
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#ffffff', edgecolor='#e2e8f0', alpha=0.95),
            zorder=5
        )

    ax.set_xlabel('Forward-Pass Inference Latency (ms)', fontweight='bold')
    ax.set_ylabel('Held-Out Test Macro-F1 (%)', fontweight='bold')
    ax.set_title('Inference Latency vs. Classification Macro-F1 Trade-Off Across Evaluated Architectures',
                 pad=14, fontweight='bold')
    ax.set_xlim(-1.5, 34)
    ax.set_ylim(y_min_plot, y_max_plot)
    ax.grid(True, linestyle='--', alpha=0.5, zorder=0)

    ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=7.8, frameon=True,
              framealpha=0.95, edgecolor='#cbd5e1')

    save_figure(fig, "Fig_17_Latency_vs_F1")


if __name__ == "__main__":
    generate_figure()
