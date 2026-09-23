"""
Figure 15: WannaCry Ransomware Evaluation on Held-Out Test Set.
Evaluates detection recall (100.0%) and mean prediction confidence (0.9297) across 157 held-out WannaCry samples,
compared with other evaluated malware families and benign subfamilies.
Reads directly from results/raw_eval_artifacts.npz and results/independent_verification_results.json.
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from analysis.figures.common_style import (
    set_springer_style, save_figure, INDEP_VERIF_JSON,
    COLOR_MALWARE, COLOR_BENIGN
)


def generate_figure():
    set_springer_style()

    with open(INDEP_VERIF_JSON, "r") as f:
        verif_data = json.load(f)

    fam_stats = verif_data["per_family_evaluation"]

    # Separate malware and benign
    fam_names = [
        ("WannaCry\n(Ransomware)", "ransomware_wannacry", True),
        ("Emotet\n(Trojan Loader)", "trojan_emotet", True),
        ("Mirai\n(IoT Worm)", "worm_mirai", True),
        ("RedLine\n(InfoStealer)", "infostealer_redline", True),
        ("CobaltStrike\n(Backdoor)", "backdoor_cobalt", True),
        ("Crypto / Archiver\n(Benign)", "benign_crypto_archiver", False),
        ("Network Client\n(Benign)", "benign_network_client", False),
        ("Packed Protector\n(Benign)", "benign_packed_protector", False),
        ("Diagnostic Tool\n(Benign)", "benign_system_diagnostic", False),
        ("System Utility\n(Benign)", "benign_utility", False),
    ]

    labels = [f[0] for f in fam_names]
    sample_counts = [fam_stats[f[1]]["sample_count"] for f in fam_names]
    det_rates = [fam_stats[f[1]]["detection_rate"] * 100 for f in fam_names]
    confidences = [fam_stats[f[1]]["mean_confidence"] for f in fam_names]

    x = np.arange(len(labels))
    width = 0.40

    fig, ax1 = plt.subplots(figsize=(11.5, 5.5), dpi=300)

    # Bars: Detection Rate (%)
    colors = ['#dc2626' if f[2] else '#2563eb' for f in fam_names]
    bars = ax1.bar(x, det_rates, width, color=colors, edgecolor='#1e293b', lw=0.9, alpha=0.90,
                   label='Correct Classification Rate (%)')

    for bar, n_spl in zip(bars, sample_counts):
        h = bar.get_height()
        ax1.annotate(f"{h:.1f}%\n(N={n_spl})",
                     xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 4), textcoords="offset points",
                     ha='center', va='bottom', fontsize=7.6, fontweight='bold', color='#1e293b')

    ax1.set_ylabel('Classification Accuracy / Detection Rate (%)', fontweight='bold')
    ax1.set_ylim(84, 122)
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, fontsize=8.0, fontweight='bold')
    ax1.grid(axis='y', linestyle='--', alpha=0.6)

    # Line: Mean Prediction Confidence
    ax2 = ax1.twinx()
    ax2.plot(x, confidences, color='#d97706', marker='D', lw=2.0, markersize=6,
             label='Mean Predicted Malware Probability (P_mal)')
    ax2.set_ylabel('Mean Model Confidence Score', color='#d97706', fontweight='bold')
    ax2.set_ylim(0.0, 1.25)
    ax2.tick_params(axis='y', labelcolor='#d97706')

    # Visual separator between Malware and Benign
    ax1.axvline(4.5, color='#94a3b8', linestyle=':', lw=1.2)
    ax1.text(2.0, 118.0, "Malware Families (Red = Malicious Verdict Target)",
             ha='center', va='center', fontsize=8.8, fontweight='bold', color='#991b1b')
    ax1.text(7.0, 118.0, "Benign Subfamilies (Blue = Benign Verdict Target)",
             ha='center', va='center', fontsize=8.8, fontweight='bold', color='#1e3a8a')

    # WannaCry Highlight Callout (arrow points to bar shoulder, completely clearing the text above the bar)
    ax1.annotate('WannaCry (157 Held-Out Samples):\n100.0% Detection Rate, Mean Conf = 0.9297',
                xy=(0.20, 97.0), xytext=(0.95, 108.5),
                arrowprops=dict(facecolor='#dc2626', shrink=0.08, width=1.0, headwidth=5),
                fontsize=7.8, fontweight='bold', color='#991b1b',
                bbox=dict(boxstyle="round,pad=0.3", fc="#fef2f2", ec="#fca5a5", lw=0.9))

    plt.title('Per-Family Detection Evaluation (Held-Out Test Set N = 1,500)',
              pad=16, fontweight='bold')

    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='lower right', frameon=True, framealpha=0.95, edgecolor='#cbd5e1')

    save_figure(fig, "Fig_15_WannaCry_Holdout")


if __name__ == "__main__":
    generate_figure()
