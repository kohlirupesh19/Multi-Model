#!/usr/bin/env python3
"""
Generate Figure 4 (fig4_robustness_analysis.pdf and Figure_4_final.pdf/png):
Dual-panel publication figure:
(a) Detection Robustness under Simulated Perturbations (N=1,000)
    F1-Score, Miss Rate (FNR), and Fall-Out (FPR) across 5 scenarios.
(b) Dynamic Attention Weight Reallocation (Opcode, CFG, Syscall attention weights).
Strict zero-fabrication: verified numbers from results/robustness_results.json.
Pristine typography and layout: rotated x-tick labels to eliminate text overlap,
clean bar gaps, and proper Greek symbols via mathtext.
"""

import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

# Font and figure styling (Springer Nature / IEEE publication grade)
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.labelsize": 11,
    "axes.titlesize": 11.5,
    "xtick.labelsize": 9.0,
    "ytick.labelsize": 9.5,
    "legend.fontsize": 9.0,
    "figure.titlesize": 12,
    "text.usetex": False,
    "mathtext.fontset": "cm"
})

def generate_figure4():
    json_path = Path("/Volumes/New Storage/Multi-Model-Binary/Multi-Model/results/robustness_results.json")
    with open(json_path, "r") as f:
        rob_data = json.load(f)

    scenarios = ["clean", "upx_packing", "dead_code_insertion", "cfg_flattening", "sandbox_stalling"]
    scenario_labels = [
        "Clean Baseline",
        "UPX-Inspired Perturbation",
        "Dead-Code NOP Perturbation",
        "CFG-Flattening Perturbation",
        "Dynamic Telemetry Dropout"
    ]

    f1_scores = [rob_data[s]["f1_score"] * 100 for s in scenarios]
    fnrs = [rob_data[s]["fnr"] * 100 for s in scenarios]
    fprs = [rob_data[s]["fpr"] * 100 for s in scenarios]

    op_alphas = [rob_data[s]["attention_distribution"]["opcode_weight"] for s in scenarios]
    cfg_alphas = [rob_data[s]["attention_distribution"]["cfg_weight"] for s in scenarios]
    sys_alphas = [rob_data[s]["attention_distribution"]["syscall_weight"] for s in scenarios]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.2, 5.4), dpi=300)

    # ---------------- Panel A: Performance under Perturbations ----------------
    x = np.arange(len(scenarios))
    width = 0.23  # Small gap between bars to prevent label touching

    r1 = ax1.bar(x - width, f1_scores, width, label='Malware-class F1-Score (%)',
                 color='#1e40af', edgecolor='#172554', lw=1.0)
    r2 = ax1.bar(x, fnrs, width, label='Miss Rate (FNR %)',
                 color='#dc2626', edgecolor='#7f1d1d', lw=1.0)
    r3 = ax1.bar(x + width, fprs, width, label='Fall-Out (FPR %)',
                 color='#d97706', edgecolor='#78350f', lw=1.0)

    # Annotate F1 scores
    for rect in r1:
        h = rect.get_height()
        ax1.annotate(f"{h:.1f}%", xy=(rect.get_x() + rect.get_width() / 2, h),
                     xytext=(0, 4), textcoords="offset points", ha='center', va='bottom',
                     fontsize=8.2, fontweight='bold', color='#1e3a8a')

    # Annotate FNR / FPR where non-zero with clean vertical offsets
    for rect, val in zip(r2, fnrs):
        if val > 0:
            ax1.annotate(f"{val:.1f}%", xy=(rect.get_x() + rect.get_width() / 2, val),
                         xytext=(0, 4), textcoords="offset points", ha='center', va='bottom',
                         fontsize=8.0, fontweight='bold', color='#991b1b')

    for rect, val in zip(r3, fprs):
        if val > 0:
            ax1.annotate(f"{val:.1f}%", xy=(rect.get_x() + rect.get_width() / 2, val),
                         xytext=(0, 4), textcoords="offset points", ha='center', va='bottom',
                         fontsize=8.0, fontweight='bold', color='#92400e')

    ax1.set_title('(a) Detection Robustness under Simulated Perturbations (N=1,000)', pad=14, fontweight='bold')
    ax1.set_ylabel('Rate / Score (%)', fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(scenario_labels, rotation=18, ha='right', fontweight='bold')
    ax1.set_ylim(0, 140)
    ax1.grid(axis='y', linestyle='--', alpha=0.5)
    ax1.legend(loc='upper center', bbox_to_anchor=(0.50, 0.98), ncol=3,
               frameon=True, framealpha=0.95, edgecolor='#cbd5e1')

    # ---------------- Panel B: Dynamic Attention Reallocation ----------------
    bar_width = 0.44
    p1 = ax2.bar(x, op_alphas, bar_width, label=r'Opcode Stream Weight ($\alpha_o$)',
                 color='#7c3aed', edgecolor='#4c1d95', lw=1.0)
    p2 = ax2.bar(x, cfg_alphas, bar_width, bottom=op_alphas, label=r'CFG Graph Weight ($\alpha_g$)',
                 color='#059669', edgecolor='#064e3b', lw=1.0)
    p3 = ax2.bar(x, sys_alphas, bar_width, bottom=np.array(op_alphas) + np.array(cfg_alphas),
                 label=r'Syscall Sequence Weight ($\alpha_s$)', color='#d97706', edgecolor='#78350f', lw=1.0)

    # Dead-Code NOP Allocation Callout (Issue 1)
    ax2.annotate(r'Dead-Code NOP Allocation:' + '\n' + r'$\alpha_o = 0.528, \alpha_g = 0.206, \alpha_s = 0.267$',
                 xy=(2.0, 1.00), xytext=(2.0, 1.18),
                 arrowprops=dict(facecolor='#1e293b', shrink=0.08, width=0.9, headwidth=4.5),
                 ha='center', va='center',
                 fontsize=7.8, fontweight='bold', color='#0f172a',
                 bbox=dict(boxstyle="round,pad=0.35", fc="#f8fafc", ec="#94a3b8", lw=0.9))

    # Dynamic Modality Fallback Callout with pristine math formatting
    ax2.annotate(r'$\alpha_s = 0.00$ (Syscall Clamped)' + '\n(Dynamic Modality Fallback)',
                 xy=(4.0, 1.00), xytext=(3.85, 1.18),
                 arrowprops=dict(facecolor='#d97706', shrink=0.08, width=0.9, headwidth=4.5),
                 ha='center', va='center',
                 fontsize=7.8, fontweight='bold', color='#78350f',
                 bbox=dict(boxstyle="round,pad=0.35", fc="#fffbeb", ec="#fde68a", lw=0.9))

    ax2.set_title('(b) Dynamic Attention Weight Reallocation', pad=14, fontweight='bold')
    ax2.set_ylabel(r'Normalized Attention Weight ($\alpha$)', fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(scenario_labels, rotation=18, ha='right', fontweight='bold')
    ax2.set_ylim(0, 1.42)
    ax2.grid(axis='y', linestyle='--', alpha=0.5)
    ax2.legend(loc='upper center', bbox_to_anchor=(0.50, 0.98), ncol=3,
               frameon=True, framealpha=0.95, edgecolor='#cbd5e1', fontsize=8.0)

    plt.tight_layout()

    # Paths to save
    p_latex = Path("/Volumes/New Storage/Multi-Model-Binary/jcmm-template LaTex/figures/fig4_robustness_analysis.pdf")
    p_pdf = Path("/Volumes/New Storage/Multi-Model-Binary/Figure_4_final.pdf")
    p_png = Path("/Volumes/New Storage/Multi-Model-Binary/Figure_4_final.png")
    p_artifact = Path("/Users/rupesh/.gemini/antigravity-ide/brain/7e42ac02-7cf0-4fa8-a810-4685f31a9a8d/Figure_4_final.png")

    fig.savefig(p_latex, bbox_inches='tight')
    fig.savefig(p_pdf, bbox_inches='tight')
    fig.savefig(p_png, dpi=300, bbox_inches='tight')
    fig.savefig(p_artifact, dpi=300, bbox_inches='tight')
    plt.close(fig)

    print(f"Generated Figure 4 successfully:")
    print(f"  {p_latex}")
    print(f"  {p_pdf}")
    print(f"  {p_png}")
    print(f"  {p_artifact}")

if __name__ == "__main__":
    generate_figure4()
