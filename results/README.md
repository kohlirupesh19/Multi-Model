# Experimental Results & Evaluation Artifacts

This directory contains serialized evaluation outputs, machine-readable metrics, formatted tables, generated figures, and latency benchmark logs.

## Directory Structure

```
results/
├── README.md                          # This documentation guide
├── FINAL_RESULTS.csv                  # Master summary table across all baseline and proposed models
├── raw_eval_artifacts.npz             # Raw predictions (y_true, y_pred, y_prob, z_fused, alphas)
├── evaluation_test.json               # Full evaluation metrics on nominal test split (1,500 samples)
├── evaluation_temporal.json           # Chronological drift evaluation metrics across 4 quarters
├── evaluation_family_holdout.json     # Zero-day single-family holdout evaluation metrics (WannaCry)
├── robustness_results.json            # Evasion and obfuscation stress test metrics (UPX, dead-code)
├── latency_benchmark.json             # Component and end-to-end CPU latency measurements
│
├── metrics/                           # Machine-readable metric JSON and CSV files
│   ├── standard_metrics.json          # Primary classification metrics and confusion matrix
│   ├── statistical_metrics.json       # Wilson score and Bootstrap percentile confidence intervals
│   ├── confidence_intervals.json      # Precomputed confidence interval bounds
│   ├── mcnemar_rf_comparison.json     # McNemar 2x2 contingency table vs Random Forest
│   ├── mcnemar_statistical_tests.json # Chi-squared statistics across all pairwise baselines
│   ├── seed_disjoint_metrics.json     # Generator-seed-disjoint OOD evaluation metrics
│   ├── component_ablation.csv         # Ablation study without InfoNCE, without GRAM, uniform fusion
│   ├── modality_ablation_comparison.json # Unimodal vs multimodal ablation metrics
│   ├── robustness.csv                 # Tabular robustness metrics under evasion attacks
│   └── numerical_dictionary.csv       # Audited master numerical dictionary
│
├── tables/                            # Formatted evaluation tables (CSV format)
│   ├── table01_dataset_composition.csv
│   ├── table02_class_family_distribution.csv
│   ├── table03_primary_performance.csv
│   ├── table04_baseline_comparison.csv
│   ├── table05_component_ablation.csv
│   ├── table06_modality_ablation.csv
│   ├── table07_robustness.csv
│   ├── table08_family_holdout.csv
│   ├── table09_temporal_evaluation.csv
│   ├── table10_latency_breakdown.csv
│   └── table11_model_complexity.csv
│
├── figures/                           # Publication-grade vector PDF and 300-DPI raster PNG figures
│   ├── Fig_01_Dataset_Flow.{pdf,png}
│   ├── Fig_03_Benchmark_Comparison.{pdf,png}
│   ├── Fig_04_Confusion_Matrix.{pdf,png}
│   ├── Fig_05_ROC_Curves.{pdf,png}
│   ├── Fig_06_PR_Curves.{pdf,png}
│   ├── Fig_07_Modality_Ablation.{pdf,png}
│   ├── Fig_13_Robustness_Analysis.{pdf,png}
│   ├── Fig_15_WannaCry_Holdout.{pdf,png}
│   ├── Fig_16_Latency_Breakdown.{pdf,png}
│   ├── Fig_17_Latency_vs_F1.{pdf,png}
│   └── Fig_18_Embedding_Visualization.{pdf,png}
│
├── benchmarks/                        # Performance and latency benchmark artifacts
│   ├── latency_benchmark.json         # Raw benchmark output
│   └── latency.csv                    # Tabular latency breakdown
│
└── logs/                              # Forensic audits, environment reports, and verification logs
    ├── dataset_audit.md               # Dataset provenance and forensic audit
    ├── environment_report.md          # Hardware, OS, and Python environment specifications
    ├── leakage_audit.md               # Split disjointness and vocabulary isolation audit
    ├── test_report.md                 # Test suite verification report
    ├── checkpoint_audit.csv           # Model parameter count and checkpoint integrity
    ├── claim_evidence_matrix.csv      # Computational claim-to-artifact mapping
    └── statistical_audit_report.md    # Statistical tests and effect size documentation
```
