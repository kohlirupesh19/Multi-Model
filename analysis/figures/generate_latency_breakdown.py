"""
Figure 16: Neural Forward-Pass Latency Decomposition.
Profiles individual neural modules and end-to-end forward pass latency on commodity CPU hardware.
Strictly labeled as Neural Forward-Pass Latency (excluding external sandbox tracing execution).
Reads directly from results/latency_benchmark.json.
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from analysis.figures.common_style import (
    set_springer_style, save_figure, LATENCY_JSON,
    COLOR_OPCODE, COLOR_CFG, COLOR_SYSCALL, COLOR_FUSION, COLOR_PROPOSED
)


def generate_figure():
    set_springer_style()

    with open(LATENCY_JSON, "r") as f:
        lat_data = json.load(f)

    lat_dict = lat_data["latencies_ms"]
    op_lat = lat_dict["opcode_transformer_ms"]        # 16.44
    cfg_lat = lat_dict["cfg_gin_ms"]                  # 0.86
    sys_lat = lat_dict["syscall_bilstm_ms"]           # 11.05
    fus_lat = lat_dict["fusion_and_classifier_ms"]    # 0.09
    total_lat = lat_dict["full_neural_forward_ms"]    # 28.87
    triage_lat = lat_dict["fast_static_triage_ms"]    # 17.53

    modules = [
        "Opcode Transformer\n(L = 2,048 Tokens)",
        "CFG GIN Encoder\n(K = 3 Graph Layers)",
        "Syscall Bi-LSTM\n(T = 512 Traces)",
        "Attention Fusion &\nMLP Classifier Head",
        "Fast Static Triage\n(Opcode + CFG Only)",
        "Full Tri-Modal\nNeural Forward Pass"
    ]
    values = [op_lat, cfg_lat, sys_lat, fus_lat, triage_lat, total_lat]
    colors = ['#7c3aed', '#059669', '#d97706', '#0891b2', '#2563eb', '#1e40af']

    x = np.arange(len(modules))
    width = 0.50

    fig, ax = plt.subplots(figsize=(10.0, 5.2), dpi=300)

    bars = ax.bar(x, values, width, color=colors, edgecolor='#1e293b', lw=0.9)

    for bar, val in zip(bars, values):
        h = bar.get_height()
        ax.annotate(f"{val:.2f} ms\n({val/total_lat*100:.1f}%)" if val <= total_lat else f"{val:.2f} ms",
                    xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 4), textcoords="offset points",
                    ha='center', va='bottom', fontsize=8.2, fontweight='bold', color='#1e293b')

    # Visual separator for composites
    ax.axvline(3.5, color='#94a3b8', linestyle=':', lw=1.2)
    ax.text(1.5, 37.5, "Individual Neural Modality Encoders",
            ha='center', va='center', fontsize=8.8, fontweight='bold', color='#475569')
    ax.text(4.5, 37.5, "Composite Inference Pathways",
            ha='center', va='center', fontsize=8.8, fontweight='bold', color='#1e3a8a')

    ax.set_ylabel('Inference Execution Time (Wall-Clock ms)', fontweight='bold')
    ax.set_title('Neural Forward-Pass Latency Decomposition on Commodity Workstation CPU',
                 pad=16, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(modules, fontsize=8.2, fontweight='bold')
    ax.set_ylim(0, 42)
    ax.grid(axis='y', linestyle='--', alpha=0.6)

    plt.subplots_adjust(bottom=0.14)

    fig.text(0.5, 0.02,
             "Measured on Apple Silicon Workstation CPU across 20 iterations. "
             "Note: Latency represents neural forward inference; dynamic sandbox tracing is excluded.",
             ha='center', fontsize=7.8, color='#475569')

    save_figure(fig, "Fig_16_Latency_Breakdown", copy_to_manuscript="fig13_latency_and_triage")


if __name__ == "__main__":
    generate_figure()
