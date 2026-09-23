"""
Master Figure Generation Orchestrator.
Executes all figure generation scripts sequentially to produce publication-grade
vector PDF and 300-DPI raster PNG figures.
"""

import sys
import time
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from analysis.figures import (
    generate_dataset_flow,
    generate_class_distribution,
    generate_benchmark_comparison,
    generate_confusion_matrix,
    generate_roc_curves,
    generate_pr_curves,
    generate_modality_ablation,
    generate_gram_infonce_ablation,
    generate_gin_depth,
    generate_token_length,
    generate_temperature,
    generate_upx_robustness,
    generate_robustness_analysis,
    generate_generalization_protocols,
    generate_wannacry_holdout,
    generate_latency_breakdown,
    generate_latency_vs_f1,
    generate_embedding_visualization,
)

# Pipeline of active figures used in the Springer manuscript
FIGURE_PIPELINE = [
    ("Figure 01: Dataset / Split Flow", generate_dataset_flow.generate_figure),
    ("Figure 03: Main Benchmark Comparison", generate_benchmark_comparison.generate_figure),
    ("Figure 04: Raw & Normalized Confusion Matrix", generate_confusion_matrix.generate_figure),
    ("Figure 05: ROC Curves & Verified AUC", generate_roc_curves.generate_figure),
    ("Figure 06: Precision-Recall Curves & Iso-F1", generate_pr_curves.generate_figure),
    ("Figure 07: Multi-Modal Modality Ablation", generate_modality_ablation.generate_figure),
    ("Figure 13: Robustness Analysis & Dynamic Attention", generate_robustness_analysis.generate_figure),
    ("Figure 15: WannaCry Ransomware Evaluation", generate_wannacry_holdout.generate_figure),
    ("Figure 16: Neural Forward-Pass Latency Decomposition", generate_latency_breakdown.generate_figure),
    ("Figure 17: Latency vs. Macro-F1 Pareto Analysis", generate_latency_vs_f1.generate_figure),
    ("Figure 18: Latent Representation Manifold Visualization", generate_embedding_visualization.generate_figure),
]


def run_all():
    print("=" * 80)
    print("EXECUTING MASTER SCIENTIFIC FIGURE GENERATION PIPELINE")
    print("=" * 80)

    start_time = time.time()
    success_count = 0
    total = len(FIGURE_PIPELINE)

    for idx, (title, func) in enumerate(FIGURE_PIPELINE, 1):
        print(f"\n[{idx:02d}/{total:02d}] Generating {title}...")
        try:
            func()
            success_count += 1
            print(f"  --> SUCCESS")
        except Exception as e:
            print(f"  --> FAILED with error: {e}")
            raise e

    elapsed = time.time() - start_time
    print("\n" + "=" * 80)
    print(f"FIGURE GENERATION COMPLETE: {success_count}/{total} figures successfully created in {elapsed:.2f}s")
    print(f"Output Directory: {PROJECT_ROOT / 'analysis' / 'figures' / 'output'}")
    print("=" * 80)


if __name__ == "__main__":
    run_all()
