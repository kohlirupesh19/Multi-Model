"""
Figure 7: Multi-Modal Ablation Analysis on Held-Out Test Set.
Evaluates Accuracy, Macro-F1, and Recall across executed modality configurations:
Tri-Modal (Full), w/o Syscall (Static Only), w/o CFG, w/o Opcode, and Unimodal Baselines.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from analysis.figures.common_style import (
    set_springer_style, save_figure, FINAL_RESULTS_CSV,
    COLOR_PROPOSED, COLOR_OPCODE, COLOR_CFG, COLOR_SYSCALL
)


def generate_figure():
    set_springer_style()

    df = pd.read_csv(FINAL_RESULTS_CSV)

    ablation_items = [
        ("Tri-Modal (Proposed)\n[Opcode + CFG + Syscall]", "EXP-01-PROPOSED-TEST"),
        ("w/o Syscall (Static Only)\n[Opcode + CFG]", "EXP-14-ABL-NO-SYSCALL"),
        ("w/o Volumetric GRAM\n[InfoNCE + Attention]", "EXP-11-ABL-NO-GRAM"),
        ("w/o InfoNCE Alignment\n[GRAM + Attention]", "EXP-15-ABL-NO-INFONCE"),
        ("w/o CFG Graph Encoder\n[Opcode + Syscall]", "EXP-13-ABL-NO-CFG"),
        ("w/o Opcode Transformer\n[CFG + Syscall]", "EXP-12-ABL-NO-OPCODE"),
        ("Opcode Only (Unimodal)", "EXP-16-BASELINE-OPCODE"),
        ("CFG Only (Unimodal)", "EXP-17-BASELINE-CFG"),
        ("Syscall Only (Unimodal)", "EXP-18-BASELINE-SYSCALL")
    ]

    names, accs, f1s, recs = [], [], [], []
    for label, exp_id in ablation_items:
        row = df[df["experiment_id"] == exp_id]
        if len(row) > 0:
            names.append(label)
            accs.append(row["accuracy"].values[0] * 100)
            f1s.append(row["F1"].values[0] * 100)
            recs.append(row["recall"].values[0] * 100)

    # Invert order for top-to-bottom reading
    names = names[::-1]
    accs = accs[::-1]
    f1s = f1s[::-1]
    recs = recs[::-1]

    y = np.arange(len(names))
    height = 0.25

    fig, ax = plt.subplots(figsize=(10.2, 6.4), dpi=300)

    rects1 = ax.barh(y + height, accs, height, label='Accuracy (%)',
                     color='#1e40af', edgecolor='#172554', lw=0.9)
    rects2 = ax.barh(y, f1s, height, label='Macro-F1 (%)',
                     color='#7c3aed', edgecolor='#4c1d95', lw=0.9)
    rects3 = ax.barh(y - height, recs, height, label='Recall (%)',
                     color='#059669', edgecolor='#064e3b', lw=0.9)

    # Annotate F1 scores
    for i, val in enumerate(f1s):
        ax.text(val + 0.6, y[i], f"{val:.2f}%", va='center', fontsize=8.0,
                fontweight='bold', color='#4c1d95')

    ax.set_xlabel('Performance Metric (%)', fontweight='bold')
    ax.set_title('Modality and Alignment Ablation Evaluation (Held-Out Test Set, N = 1,500)',
                 pad=14, fontweight='bold')
    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=8.5, fontweight='bold')
    ax.set_xlim(70, 108)
    ax.grid(axis='x', linestyle='--', alpha=0.6)
    ax.legend(loc='lower right', frameon=True, framealpha=0.95, edgecolor='#cbd5e1')

    save_figure(fig, "Fig_07_Modality_Ablation", copy_to_manuscript="fig12_ablation_waterfall")


if __name__ == "__main__":
    generate_figure()
