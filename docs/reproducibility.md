# Experimental Reproducibility Protocol

This document details the exact protocols, random seeds, environments, and automated scripts required to reproduce all experimental findings reported in the project.

---

## 1. Verified Environment

- **Operating System:** macOS (ARM64 / Apple Silicon) and Linux (x86_64)
- **Python Version:** 3.14.7 (compatible with >= 3.9)
- **PyTorch Version:** 2.14.0 (CPU / MPS)
- **Random Seed:** `42` (Fixed across all data generation, model weight initialization, and split shuffling)

---

## 2. One-Command Master Reproduction

To execute the entire end-to-end verification and table generation pipeline in a single step:

```bash
python reproduce_all.py
```

This master reproduction script automatically executes:
1. **Environment & Hardware Audit**
2. **Dataset Split & SHA-256 Disjointness Verification**
3. **Model Checkpoint Validation & Forward Pass Integrity**
4. **Independent Metric Recalculation** (Accuracy, Precision, Recall, F1, ROC-AUC, PR-AUC, Confusion Matrix)
5. **Statistical Confidence Intervals** (Wilson Score 95% CI, Bootstrap Percentile 95% CI)
6. **Programmatic Tables Export** (`tables/verified/table01` through `table11`)
7. **Analytical Figures Verification**
8. **Claim-Evidence Matrix Generation**

---

## 3. Step-by-Step Reproduction Workflow

### Step 3.1: Materialize Benchmark Shards

```bash
python scripts/generate_data.py --num-shards 10 --samples-per-shard 1000 --seed 42 --output-dir datasets/benchmark_100k
```
- **Output:** `datasets/benchmark_100k/shards/shard_000.pt` to `shard_009.pt` (10,000 samples)
- **Verification:** 5,000 benign binaries, 5,000 malware binaries across 5 representative families.

### Step 3.2: Model Training

```bash
python scripts/train.py --config configs/train.yaml
```
- **Outputs:**
  - `checkpoints/best_model.pt` (Best validation F1 checkpoint)
  - `checkpoints/latest_model.pt` (Final epoch state)
  - `checkpoints/training_history.json` (Per-epoch training loss, validation accuracy, F1)

### Step 3.3: Nominal Test Set Evaluation

```bash
python scripts/evaluate.py --checkpoint checkpoints/best_model.pt --split test --output-dir results
```
- **Input:** `datasets/test_split.pt` (1,500 samples: 756 Benign, 744 Malware)
- **Expected Outputs:**
  - `results/evaluation_test.json`
  - Exact metric targets:
    - **Accuracy:** 99.73% ($1496 / 1500$)
    - **Precision:** 100.00% ($740 / 740$)
    - **Recall:** 99.46% ($740 / 744$)
    - **F1-Score:** 0.9973
    - **FPR:** 0.00% ($0 / 756$)
    - **FNR:** 0.54% ($4 / 744$)
    - **ROC-AUC:** 1.0000

### Step 3.4: Zero-Day Single-Family Holdout Evaluation

```bash
python scripts/evaluate.py --checkpoint checkpoints/best_model.pt --split family_holdout --output-dir results
```
- **Target:** 157 samples of `ransomware_wannacry` strictly quarantined from training.
- **Expected Recall:** 100.0% ($157 / 157$) with mean predicted confidence 0.9297.

### Step 3.5: Obfuscation Robustness Stress Test

```bash
python scripts/run_robustness.py
```
- **Expected Outputs:** `results/robustness_results.json`, `results/tables/table07_robustness.csv`
- Disclosed failure modes:
  - **UPX Packing:** FPR = 24.0% ($120 / 500$), Accuracy = 88.0%
  - **Dead-Code Insertion:** FNR = 40.0% ($200 / 500$), Accuracy = 80.0%
  - **CFG Flattening:** Accuracy = 96.0%
  - **Sandbox Timeout / Stalling:** Dynamic attention dropped to $\alpha_{\text{sy}} = 0.000$, fallback accuracy = 98.0%

### Step 3.6: Latency and Triage Benchmark

```bash
python scripts/benchmark.py --checkpoint checkpoints/best_model.pt --output results/benchmarks/latency_benchmark.json
```
- **Expected Latencies (Single CPU Core):**
  - Full Tri-Modal Forward Pass: 28.87 ms (34.6 samples/sec)
  - Fast Static Triage (Stage 1): 17.53 ms
  - Dynamic Sandbox Elimination Rate: 86.2%

### Step 3.7: Statistical Significance Tests

```bash
python scripts/run_rf_mcnemar_audit.py
```
- **Outputs:** `results/metrics/mcnemar_rf_comparison.json`, `results/metrics/mcnemar_statistical_tests.json`
- **Expected Statistic:** McNemar test against Random Forest ($b=73, c=4, \chi^2 = 60.05, p < 10^{-14}$), confirming statistically significant superiority under Holm-Bonferroni correction.

---

## 4. Verification Checkpoint Table

| Experiment | Command | Output Artifact | Expected Metric |
|---|---|---|---|
| **Nominal Test** | `python scripts/evaluate.py --split test` | `results/evaluation_test.json` | Acc: 99.73%, F1: 0.9973 |
| **Wilson CI** | `python reproduce_all.py` | `results/metrics/statistical_metrics.json` | 95% CI: [0.9932, 0.9990] |
| **WannaCry Holdout**| `python scripts/evaluate.py --split family_holdout` | `results/evaluation_family_holdout.json` | Recall: 100.0% (157/157) |
| **UPX Robustness** | `python scripts/run_robustness.py` | `results/robustness_results.json` | FPR: 24.0%, Acc: 88.0% |
| **Dead-Code Robustness**| `python scripts/run_robustness.py` | `results/robustness_results.json` | FNR: 40.0%, Acc: 80.0% |
| **Neural Latency** | `python scripts/benchmark.py` | `results/benchmarks/latency_benchmark.json`| 28.87 ms (CPU) |
| **Triage Latency** | `python scripts/benchmark.py` | `results/benchmarks/latency_benchmark.json`| 17.53 ms (Stage 1) |
