# Computational Result Verification Guide

This document provides a transparent, zero-fabrication verification map linking all computational claims to their exact repository artifacts, evaluation scripts, configurations, and test logs.

---

## 1. Master Verification Map

| Computational Claim | Repository Artifact | Evaluation Script | Configuration | Output Verification Artifact | Verification Status |
|---|---|---|---|---|:---:|
| **1. 100K Catalog Manifest & 10K Materialized Cohort** | `datasets/manifests/dataset_manifest.jsonl`, `datasets/benchmark_100k/shards/` | `scripts/generate_data.py` | `configs/default.yaml` | `datasets/benchmark_100k/dataset_summary.json` | **VERIFIED** |
| **2. Deterministic 70/15/15 Data Partitioning** | `datasets/train_split.pt`, `datasets/val_split.pt`, `datasets/test_split.pt` | `scripts/generate_dataset.py` | `configs/train.yaml` | `results/tables/table01_dataset_composition.csv` | **VERIFIED** |
| **3. Clean Test Accuracy: 99.73% (1,496 / 1,500)** | `results/raw_eval_artifacts.npz` | `scripts/evaluate.py` | `configs/evaluation.yaml` | `results/metrics/standard_metrics.json`, `results/evaluation_test.json` | **VERIFIED** |
| **4. Test Precision: 100.0%, Clean FPR: 0.00%** | `results/raw_eval_artifacts.npz` ($FP=0$) | `scripts/evaluate.py` | `configs/evaluation.yaml` | `results/metrics/standard_metrics.json` | **VERIFIED** |
| **5. Test Recall: 99.46% (740 / 744, FN: 4)** | `results/raw_eval_artifacts.npz` ($FN=4$) | `scripts/evaluate.py` | `configs/evaluation.yaml` | `results/metrics/standard_metrics.json` | **VERIFIED** |
| **6. Wilson Score 95% CI: [99.32%, 99.90%]** | `results/metrics/statistical_metrics.json` | `reproduce_all.py` | `configs/evaluation.yaml` | `results/metrics/confidence_intervals.json` | **VERIFIED** |
| **7. Bootstrap Percentile 95% F1 CI: [0.9946, 0.9993]** | `results/metrics/statistical_metrics.json` | `reproduce_all.py` | `configs/evaluation.yaml` | `results/metrics/confidence_intervals.json` | **VERIFIED** |
| **8. WannaCry Zero-Day Holdout Recall: 100.0% (157 / 157)** | `results/evaluation_family_holdout.json` | `scripts/evaluate.py` | `configs/evaluation.yaml` | `results/tables/table08_family_holdout.csv` | **VERIFIED** |
| **9. Disclosed UPX Packing Robustness: 24.0% FPR** | `results/robustness_results.json` | `scripts/run_robustness.py` | `configs/evaluation.yaml` | `results/tables/table07_robustness.csv` | **VERIFIED** |
| **10. Disclosed Dead-Code Insertion Robustness: 40.0% FNR** | `results/robustness_results.json` | `scripts/run_robustness.py` | `configs/evaluation.yaml` | `results/tables/table07_robustness.csv` | **VERIFIED** |
| **11. Full Neural Forward Pass Latency: 28.87 ms (CPU)** | `results/benchmarks/latency_benchmark.json` | `scripts/benchmark.py` | `configs/inference.yaml` | `results/benchmarks/latency.csv` | **VERIFIED** |
| **12. Fast Static Triage Latency: 17.53 ms (86.2% yield)** | `results/benchmarks/latency_benchmark.json` | `scripts/benchmark.py` | `configs/inference.yaml` | `results/tables/table10_latency_breakdown.csv` | **VERIFIED** |
| **13. Chronological Drift Stability across 4 Quarters** | `results/evaluation_temporal.json` | `scripts/evaluate.py` | `configs/evaluation.yaml` | `results/tables/table09_temporal_evaluation.csv` | **VERIFIED** |
| **14. McNemar Statistical Significance vs Random Forest** | `results/metrics/mcnemar_rf_comparison.json` | `scripts/run_rf_mcnemar_audit.py` | `configs/evaluation.yaml` | `results/metrics/mcnemar_statistical_tests.json` ($\chi^2=60.05, p < 10^{-14}$) | **VERIFIED** |
| **15. Trained Neural Checkpoint Availability** | `checkpoints/best_model.pt` (7.26 MB) | `scripts/inference.py` | `configs/inference.yaml` | `checkpoints/model_manifest.json`, `checkpoints/training_history.json` | **VERIFIED** |

---

## 2. Independent Verification Command

Any independent researcher or editor can verify the entire suite using:

```bash
# Verify all automated unit and consistency tests (68 tests)
pytest tests

# Verify numerical alignment across dataset splits and metrics
python reproduce_all.py
```
