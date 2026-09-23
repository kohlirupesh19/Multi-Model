# Experimental Results & Raw Evaluation Artifacts

This directory contains the serialized evaluation results, curve data, and raw evaluation artifacts generated across all benchmark experiments.

## Files

| File | Format | Description |
|---|---|---|
| [`raw_eval_artifacts.npz`](./raw_eval_artifacts.npz) | NumPy compressed archive | Raw predictions, ground truth labels, predicted probabilities, and family annotations across all 1,500 test split samples |
| [`roc_curves.csv`](./roc_curves.csv) | CSV | ROC curve operating points (FPR, TPR, Thresholds) |
| [`pr_curves.csv`](./pr_curves.csv) | CSV | Precision-Recall curve operating points (Precision, Recall, Thresholds) |
| [`evaluation_test.json`](./evaluation_test.json) | JSON | Complete test evaluation metrics (Accuracy: 99.7333%, Precision: 1.0, Recall: 0.9946, F1: 0.9973, ROC-AUC: 1.0, PR-AUC: 1.0) |
| [`evaluation_family_holdout.json`](./evaluation_family_holdout.json) | JSON | Family-disjoint and zero-day holdout evaluation metrics (157 sample-level WannaCry test samples, 100% recall) |
| [`evaluation_temporal.json`](./evaluation_temporal.json) | JSON | Temporal generalization evaluation across time-partitioned binaries |
| [`robustness_results.json`](./robustness_results.json) | JSON | Adversarial and obfuscation robustness evaluation (UPX, instruction substitution, dead-code injection) |
| [`latency_benchmark.json`](./latency_benchmark.json) | JSON | End-to-end hardware latency profiling across CPU and GPU configurations |
| [`independent_verification_results.json`](./independent_verification_results.json) | JSON | Results of independent metric re-computation from raw model forward passes |
