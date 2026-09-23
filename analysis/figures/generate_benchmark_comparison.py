"""
Figure 3: Main Benchmark Comparison on Held-Out Test Split.
Grouped bar chart comparing Accuracy, Precision, Recall, and Macro-F1 across verified models.
Explicitly distinguishes Reproduced Experiments from Literature Baselines.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from analysis.figures.common_style import (
    set_springer_style, save_figure, FINAL_RESULTS_CSV,
    COLOR_PROPOSED, COLOR_OPCODE, COLOR_CFG, COLOR_SYSCALL, COLOR_BASELINE
)


def generate_figure():
    set_springer_style()

    # Load verified experimental results
    df = pd.read_csv(FINAL_RESULTS_CSV)

    # Filter models to compare on the held-out test set
    models_data = [
        # Proposed
        ("Proposed Multi-Modal\n(Tri-Modal + GRAM)", "EXP-01-PROPOSED-TEST", "Reproduced (Ours)"),
        # Baselines: Ablations / Unimodal
        ("Early Concat MLP\n(Feature Concat)", "EXP-22-BASELINE-CONCAT", "Reproduced Baseline"),
        ("Opcode Transf.\n(Unimodal)", "EXP-16-BASELINE-OPCODE", "Reproduced Baseline"),
        ("CFG GIN\n(Unimodal)", "EXP-17-BASELINE-CFG", "Reproduced Baseline"),
        ("Syscall Bi-LSTM\n(Unimodal)", "EXP-18-BASELINE-SYSCALL", "Reproduced Baseline"),
        # Literature Baselines
        ("MalConv (2020)\n(Gated CNN)", "EXP-19-BASELINE-MALCONV", "Literature Baseline"),
        ("Asm2Vec (2019)\n(Disassembly PV)", "EXP-21-BASELINE-ASM2VEC", "Literature Baseline"),
        ("Gemini (2019)\n(Structure2Vec)", "EXP-20-BASELINE-GEMINI", "Literature Baseline"),
    ]

    labels = []
    accs, precs, recs, f1s = [], [], [], []
    categories = []

    for name, exp_id, cat in models_data:
        row = df[df["experiment_id"] == exp_id]
        if len(row) > 0:
            labels.append(name)
            accs.append(row["accuracy"].values[0] * 100)
            precs.append(row["precision"].values[0] * 100)
            recs.append(row["recall"].values[0] * 100)
            f1s.append(row["F1"].values[0] * 100)
            categories.append(cat)

    x = np.arange(len(labels))
    width = 0.20

    fig, ax = plt.subplots(figsize=(12.0, 5.8), dpi=300)

    rects1 = ax.bar(x - 1.5 * width, accs, width, label='Accuracy (%)',
                    color='#1e40af', edgecolor='#172554', lw=0.9)
    rects2 = ax.bar(x - 0.5 * width, precs, width, label='Precision (%)',
                    color='#059669', edgecolor='#064e3b', lw=0.9)
    rects3 = ax.bar(x + 0.5 * width, recs, width, label='Recall (%)',
                    color='#d97706', edgecolor='#78350f', lw=0.9)
    rects4 = ax.bar(x + 1.5 * width, f1s, width, label='Macro-F1 (%)',
                    color='#7c3aed', edgecolor='#4c1d95', lw=0.9)

    # Highlight proposed model value on F1
    ax.annotate(f'{f1s[0]:.2f}%',
                xy=(x[0] + 1.5 * width, f1s[0]),
                xytext=(0, 4), textcoords="offset points",
                ha='center', va='bottom', fontsize=8.2, fontweight='bold', color='#4c1d95')

    # Visual separator between Reproduced and Literature baselines
    ax.axvline(4.5, color='#94a3b8', linestyle=':', lw=1.2)
    ax.text(2.0, 106.5, "Reproduced Local Experiments (Held-Out Test Partition)",
            ha='center', va='center', fontsize=9.0, fontweight='bold', color='#1e3a8a')
    ax.text(6.0, 106.5, "Literature-Reported Baseline Comparisons",
            ha='center', va='center', fontsize=9.0, fontweight='bold', color='#475569')

    ax.set_ylabel('Performance Metric (%)', fontweight='bold')
    ax.set_title('Comparative Evaluation on Held-Out Test Set (N = 1,500)',
                 pad=18, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8.2, fontweight='bold')
    ax.set_ylim(70, 110)
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    ax.legend(loc='lower right', frameon=True, framealpha=0.95, edgecolor='#cbd5e1', ncol=4)

    save_figure(fig, "Fig_03_Benchmark_Comparison")


if __name__ == "__main__":
    generate_figure()
