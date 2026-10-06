# Geometric Multimodal Representation Learning with Availability-Aware Fusion for Executable Program Analysis

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Framework: PyTorch](https://img.shields.io/badge/PyTorch-2.0+-ee4c2c.svg)](https://pytorch.org/)
[![Tests Passing](https://img.shields.io/badge/tests-74%2F74%20passing-brightgreen.svg)](multimodal_malware/tests/)
[![Journal: JCMM](https://img.shields.io/badge/Journal-JCMM-indigo.svg)](https://jcmm.org/)

Official open-source research repository and reproducibility artifacts for the manuscript:  
**"Geometric Multimodal Representation Learning with Availability-Aware Fusion for Executable Program Analysis"**  
*Journal of Computers, Mechanical and Management (JCMM)*

---

## 🎯 Research Objective

Automated binary triage in enterprise security operations requires fast, reliable discrimination between benign software and adversarial payloads. While disassembled opcode mnemonic sequences, control-flow graphs (CFGs), and dynamic API execution traces offer complementary behavioral views, integrating these heterogeneous streams faces three fundamental obstacles:
1. **Hyperspherical Modality Gaps:** High-dimensional discrepancy and representation drift between sequential and graph-structured modalities.
2. **Multi-View Geometric Collapse:** Independent pairwise contrastive objectives (e.g., standard InfoNCE) leave the joint volume spanned by all three modalities unregularized.
3. **Telemetry Dropout & Modality Scarcity:** Dynamic sandbox detonation frequently times out, crashes, or is bypassed by anti-analysis evasion, resulting in missing execution streams.

This framework introduces an end-to-end tri-modal representation learning architecture coupled with:
- **Volumetric Gramian Representation Alignment Measure (GRAM):** Minimizes the 3-dimensional parallelotope volume $\det(G^+)$ of positive triplets while repelling mismatched triplets via $-\lambda_{\text{sep}} \log(1 + \det G^-)$ to enforce collinear consensus on $\mathbb{S}^{127}$.
- **Availability-Aware Dynamic Attention Gating:** Mathematically clamps attention weights on absent or corrupted telemetry channels ($\alpha_m \to 0$ via extreme negative logit biasing), routing 100% of decision weight across surviving static streams.

---

## 🏗️ Repository Architecture

```
Multi-Model/
├── analysis/                         # Figure generation and visualization scripts
│   └── figures/                      # Publication-quality 300-DPI PDF and PNG figure generators
├── checkpoints/                      # Trained model checkpoints & training history
│   ├── best_model.pt                 # Audited model checkpoint (537,090 parameters)
│   ├── latest_model.pt               # Terminal epoch checkpoint
│   ├── model_manifest.json           # Architecture hyperparameter specification
│   └── training_history.json         # Complete 10-epoch training loss & validation logs
├── configs/                          # Experiment configuration YAML files
│   ├── data_generation.yaml          # Synthetic benchmark generation configuration
│   ├── full_multimodal.yaml          # Full tri-modal architecture parameters
│   └── lightweight.yaml              # Lightweight CPU configuration
├── datasets/                         # Benchmark datasets and splits
│   ├── benchmark_100k/               # 100,000-record catalog manifest and 10 active shards
│   ├── train_split.pt                # 7,000 nominal training samples
│   ├── val_split.pt                  # 1,500 validation samples
│   ├── test_split.pt                 # 1,500 nominal held-out test samples
│   └── seed_disjoint_test_split.pt   # 1,500 generator-seed-disjoint test samples (unseen seeds)
├── docs/                             # Detailed technical documentation
│   └── data_generation.md            # Synthetic benchmark algorithmic specification
├── multimodal_malware/               # Core Python package
│   ├── models/                       # Neural encoders (Transformer, GIN, BiLSTM, Fusion, GRAM)
│   ├── features/                     # Tokenizers & extractors (Opcode, CFG, Syscall, PE metadata)
│   ├── training/                     # Dataset loaders, loss functions, trainer
│   ├── evaluation/                   # Latency, robustness, and metric evaluation modules
│   └── tests/                        # 74 automated pytest regression tests
├── results/                          # Machine-readable evaluation outputs
│   ├── verified/                     # Canonical benchmark metrics (JSON & CSV)
│   ├── raw_eval_artifacts.npz        # Raw logits, true labels, predicted probabilities
│   ├── robustness_results.json       # 5-condition adversarial perturbation metrics
│   ├── evaluation_test.json          # Complete nominal test evaluation report
│   ├── roc_curves.csv                # ROC curve evaluation coordinates
│   └── pr_curves.csv                 # PR curve evaluation coordinates
├── scripts/                          # Executable evaluation & reproduction CLI scripts
│   ├── generate_dataset.py           # Deterministic benchmark generator CLI
│   ├── run_rf_mcnemar_audit.py       # Random Forest baseline & paired McNemar test
│   ├── run_modality_ablation_audit.py # Availability masking vs raw zeroing audit
│   └── independent_metric_verification.py # Independent metric recalculation
├── reproduce_all.py                  # Master reproduction script
├── requirements.txt                  # Python dependency specifications
└── README.md                         # Project documentation
```

---

## ⚡ Quickstart & Environment Setup

### 1. Requirements & Installation
Tested on Python 3.10, 3.11, 3.12, 3.13, and 3.14 on macOS and Linux:
```bash
git clone https://github.com/kohlirupesh19/Multi-Model.git
cd Multi-Model
pip install -r requirements.txt
```

### 2. Verify Benchmark Determinism
Verify that the synthetic generator is strictly deterministic ($O(1)$ index binding):
```bash
python scripts/generate_dataset.py --verify-determinism
```
*Expected Output:* `✓ Determinism test PASSED: Same index -> Identical hash; Distinct index -> Distinct hash.`

---

## 🔬 1-Click Verification Commands

### 1. Independent Metric Recalculation
Evaluates the trained checkpoint `checkpoints/best_model.pt` across all 1,500 test samples in `datasets/test_split.pt` and recalculates exact metrics and Wilson score confidence intervals:
```bash
python INDEPENDENT_METRIC_VERIFICATION.py
```
*Expected Output:*
- Accuracy: **99.7333%** ($TP = 740, TN = 756, FP = 0, FN = 4$)
- Precision: **100.00%** (Wilson 95% CI: $[0.9948, 1.0000]$)
- Recall: **99.4624%** (Wilson 95% CI: $[0.9863, 0.9979]$)
- Macro-F1: **0.9973** (Wilson 95% CI: $[0.9931, 0.9989]$)
- ROC-AUC / PR-AUC: **1.0000** / **1.0000**

### 2. Run Automated Regression Test Suite (74 Tests)
Executes all unit, integration, and mathematical parity tests (including Equation 11 analytical verification):
```bash
pytest multimodal_malware/tests/
```
*Status: 74/74 tests pass cleanly.*

### 3. Paired McNemar Test Against Random Forest Baseline
Extracts 11 handcrafted summary statistics, fits Random Forest (100 trees), evaluates on identical 1,500 test instances, and executes McNemar's test:
```bash
python scripts/run_rf_mcnemar_audit.py
```
*Expected Output:*
- Random Forest Accuracy: **95.13%**, Macro-F1: **0.9513**
- Contingency Table: Both Correct = 1,423; RF Correct / Proposed Wrong = 4; RF Wrong / Proposed Correct = 73; Both Wrong = 0
- McNemar $\chi^2 = 60.0519$, Exact Binomial $p = 1.89 \times 10^{-17} < 0.001$ (Statistically Significant)

### 4. Modality Ablation & Availability Mask Audit
Evaluates dynamic telemetry dropouts and compares availability-aware masking against raw feature zeroing:
```bash
python scripts/run_modality_ablation_audit.py
```

### 5. Regenerate Publication Figures
Regenerates all figures programmatically from raw evaluation artifacts:
```bash
python -m analysis.figures.generate_robustness_analysis
python -m analysis.figures.generate_gram_surface_3d
python -m analysis.figures.generate_latency_breakdown
python -m analysis.figures.generate_confusion_matrix
```

---

## 📊 Summary of Experimental Findings

| Dimension | Primary Metric / Verified Value | Source Artifact |
| :--- | :--- | :--- |
| **Nominal Test Cohort** | $N = 1,500$ held-out binaries (756 Benign, 744 Malware) | `datasets/test_split.pt` |
| **Confusion Matrix** | $TP = 740, \quad TN = 756, \quad FP = 0, \quad FN = 4$ | `results/raw_eval_artifacts.npz` |
| **Classification Accuracy** | **99.7333%** (Wilson 95% CI: $[99.32\%, 99.90\%]$) | `results/verified/standard_metrics.json` |
| **Precision & Clean FPR** | Precision: **100.0%**; Clean FPR: **0.00%** (Wilson: $[0.00\%, 0.51\%]$) | `results/verified/standard_metrics.json` |
| **Recall & Clean FNR** | Recall: **99.4624%**; Clean FNR: **0.5376%** ($4$ FN) | `results/verified/standard_metrics.json` |
| **Macro F1-Score** | **0.9973** (Wilson 95% CI: $[0.9931, 0.9989]$) | `results/verified/standard_metrics.json` |
| **ROC-AUC & PR-AUC** | **1.0000** & **1.0000** (Empirical AUC: 0.999995) | `results/roc_curves.csv`, `pr_curves.csv` |
| **Seed-Disjoint Generalization** | **99.3333%** Accuracy, **99.33%** F1 ($TP=740, TN=750, FN=10, FP=0$) | `results/verified/seed_disjoint_metrics.json` |
| **Single-Family Holdout** | WannaCry (157 test samples): **100.0% Recall** (Mean Conf: 0.9297) | `results/verified/family_holdout_metrics.json` |
| **Static Triage Mode ($m_s=0$)** | **99.47%** Accuracy, **99.47%** F1 ($TP=736, TN=756, FN=8, FP=0$) | `results/verified/modality_ablation_comparison.json` |
| **Neural Forward Latency** | **28.87 ms** on CPU (Throughput: $34.6$ samples/sec) | `results/verified/latency.csv` |
| **Fast Static Triage Latency** | **17.53 ms** on CPU (Throughput: $57.0$ samples/sec) | `results/verified/latency.csv` |
| **GRAM Loss Trajectory** | Monotonic decrease from $0.9126$ (Epoch 1) to $-0.0115$ (Epoch 10) | `checkpoints/training_history.json` |

---

## ⚠️ Limitations & Construct Validity Disclosures

1. **Synthetic Feature-Level Benchmark:** Experimental samples are deterministically synthesized to model statistical distributions of PE binaries informed by EMBER, SOREL-20M, and BODMAS literature, rather than physical PE executable files compiled on disk.
2. **Preprocessing Excluded from Latency:** Reported latencies (28.87 ms full; 17.53 ms static) measure neural forward inference on commodity CPUs and exclude physical PE parsing, disassembly, graph construction, and hypervisor sandbox detonation.
3. **Simulated vs. Physical Obfuscations:** Evasion evaluations represent in-memory token/edge tensor corruptions rather than binary recompilation via obfuscators (e.g., Tigress, OLLVM).

---

## 📜 Citation

```bibtex
@article{kohli2026geometric,
  author    = {Kohli, Rupesh and Bhabad, Harish Parshuram},
  title     = {{Geometric Multimodal Representation Learning with Availability-Aware Fusion for Executable Program Analysis}},
  journal   = {Journal of Computers, Mechanical and Management},
  year      = {2026},
  volume    = {X},
  number    = {Y},
  pages     = {Z},
  publisher = {Journal of Computers, Mechanical and Management}
}
```
