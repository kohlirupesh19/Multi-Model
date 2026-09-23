"""
Figure 13: Multi-Modal Obfuscation Robustness & Dynamic Attention Reallocation.
Dual panel:
Panel A: Evasion Benchmark (F1-score, FNR, and FPR across Clean, UPX, Dead-Code, CFG Flattening, Sandbox Stalling).
Panel B: Dynamic Attention Reallocation (Opcode, CFG, Syscall attention weights across all 5 scenarios).
Reads directly from results/robustness_results.json.
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from analysis.figures.common_style import (
    set_springer_style, save_figure, ROBUSTNESS_JSON,
    COLOR_OPCODE, COLOR_CFG, COLOR_SYSCALL
)


def generate_figure():
    set_springer_style()

    with open(ROBUSTNESS_JSON, "r") as f:
        rob_data = json.load(f)

    scenarios = ["clean", "upx_packing", "dead_code_insertion", "cfg_flattening", "sandbox_stalling"]
    scenario_names = ["Clean\n(Baseline)", "UPX\nPacking", "Dead-Code\nInsertion", "CFG\nFlattening", "Sandbox\nStalling"]

    f1_scores = [rob_data[s]["f1_score"] * 100 for s in scenarios]
    fnrs = [rob_data[s]["fnr"] * 100 for s in scenarios]
    fprs = [rob_data[s]["fpr"] * 100 for s in scenarios]

    op_alphas = [rob_data[s]["attention_distribution"]["opcode_weight"] for s in scenarios]
    cfg_alphas = [rob_data[s]["attention_distribution"]["cfg_weight"] for s in scenarios]
    sys_alphas = [rob_data[s]["attention_distribution"]["syscall_weight"] for s in scenarios]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.0, 5.2), dpi=300)

    # Panel A: Performance under Attacks
    x = np.arange(len(scenarios))
    width = 0.26

    r1 = ax1.bar(x - width, f1_scores, width, label='Macro-F1 (%)',
                 color='#1e40af', edgecolor='#172554', lw=0.9)
    r2 = ax1.bar(x, fnrs, width, label='Miss Rate (FNR %)',
                 color='#dc2626', edgecolor='#7f1d1d', lw=0.9)
    r3 = ax1.bar(x + width, fprs, width, label='Fall-Out (FPR %)',
                 color='#d97706', edgecolor='#78350f', lw=0.9)

    for rect in r1:
        h = rect.get_height()
        ax1.annotate(f"{h:.1f}%", xy=(rect.get_x() + rect.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points", ha='center', va='bottom',
                     fontsize=7.8, fontweight='bold', color='#1e3a8a')

    ax1.set_title('(a) Detection Robustness under Evasion Attacks', pad=14, fontweight='bold')
    ax1.set_ylabel('Rate / Score (%)', fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(scenario_names, fontsize=8.5, fontweight='bold')
    ax1.set_ylim(0, 130)
    ax1.grid(axis='y', linestyle='--', alpha=0.6)
    ax1.legend(loc='upper center', bbox_to_anchor=(0.50, 0.98), ncol=3,
               frameon=True, framealpha=0.95, edgecolor='#cbd5e1')

    # Panel B: Dynamic Attention Reallocation
    p1 = ax2.bar(x, op_alphas, 0.45, label='Opcode Stream Weight',
                 color='#7c3aed', edgecolor='#4c1d95', lw=0.9)
    p2 = ax2.bar(x, cfg_alphas, 0.45, bottom=op_alphas, label='CFG Graph Weight',
                 color='#059669', edgecolor='#064e3b', lw=0.9)
    p3 = ax2.bar(x, sys_alphas, 0.45, bottom=np.array(op_alphas) + np.array(cfg_alphas),
                 label='Syscall Sequence Weight', color='#d97706', edgecolor='#78350f', lw=0.9)

    # Annotate zero syscall weight on stalling cleanly above the bar
    ax2.annotate('Syscall Weight = 0.00\n(Dynamic Modality Fallback)',
                 xy=(4.0, 1.00), xytext=(3.15, 1.14),
                 arrowprops=dict(facecolor='#d97706', shrink=0.08, width=1.0, headwidth=5),
                 ha='center', va='center',
                 fontsize=7.8, fontweight='bold', color='#78350f',
                 bbox=dict(boxstyle="round,pad=0.3", fc="#fffbeb", ec="#fde68a", lw=0.9))

    ax2.set_title('(b) Dynamic Attention Weight Reallocation', pad=14, fontweight='bold')
    ax2.set_ylabel('Normalized Attention Weight (α)', fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(scenario_names, fontsize=8.5, fontweight='bold')
    ax2.set_ylim(0, 1.30)
    ax2.grid(axis='y', linestyle='--', alpha=0.6)
    ax2.legend(loc='upper left', bbox_to_anchor=(0.02, 0.98), ncol=1,
               frameon=True, framealpha=0.95, edgecolor='#cbd5e1', fontsize=8.0)

    save_figure(fig, "Fig_13_Robustness_Analysis", copy_to_manuscript="fig10_attention_reallocation")


if __name__ == "__main__":
    generate_figure()
