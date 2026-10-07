# Multimodal Malware Analysis Framework

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.2+-ee4c2c.svg)](https://pytorch.org/)
[![Tests: 68 Passing](https://img.shields.io/badge/tests-68%2F68%20passing-brightgreen.svg)](tests/)

A deep learning framework for binary executable analysis that learns geometric multimodal representations across static disassembled instructions, control flow graph topology, and dynamic system call execution traces with availability-aware attention fusion.

---

## Overview

Modern executable program analysis requires robust discrimination between benign utilities and malicious software under incomplete or evasive behavioral observations. This framework provides an end-to-end Python/PyTorch pipeline that extracts, aligns, and fuses three complementary execution modalities:

1. **Disassembled Opcode Sequences:** Captures local functional semantics using a multi-head self-attention Transformer.
2. **Control Flow Graphs (CFG):** Captures high-level execution branching and structural program flow using a Graph Isomorphism Network (GIN).
3. **Dynamic System Call Sequences:** Captures chronological runtime OS interactions via a Bidirectional LSTM.

The representations are aligned on a shared 128-dimensional hyperspherical manifold using a combined **Multi-Modal InfoNCE** and **Volumetric Gramian Alignment (GRAM)** objective, coupled with an **Availability-Aware Attention Fusion** layer that dynamically tolerates sandbox timeouts and missing telemetry.

---

## Key Components

- **Data Pipeline (`multimodal_malware/features/`):** Opcode tokenizer with importance sampling, basic-block CFG builder, and dynamic system call sequence extractor.
- **Model Encoders (`multimodal_malware/models/`):** Opcode Transformer (4 layers, $d=128$), CFG-GIN (3 layers), and Syscall Bi-LSTM (hidden dim 128).
- **Geometric Alignment (`multimodal_malware/models/`):** Contrastive InfoNCE loss ($\tau=0.07$) and Volumetric GRAM loss ($\lambda_{\text{sep}}=0.10$).
- **Adaptive Late Fusion (`attention_fusion.py`):** Dynamic attention allocation layer with masked softmax routing for telemetry dropout and missing modalities.
- **Evaluation & Benchmarking (`multimodal_malware/evaluation/`):** Threshold sweepers, ROC/PR metric evaluators, chronological temporal drift analyzer, single-family zero-day holdout evaluator, and single-CPU latency benchmark.
- **Interactive Workstation (`app.py`):** High-performance Streamlit visual workbench for single-binary inspection, attention inspection, threshold tuning, and nearest-neighbor vector similarity retrieval.

---

## Repository Structure

```
.
├── README.md                          # Project overview and user guide
├── LICENSE                            # MIT License
├── requirements.txt                   # Production dependencies
├── environment.yml                    # Conda environment specification
├── pyproject.toml                     # Python package configuration
├── reproduce_all.py                   # Master end-to-end verification script
│
├── configs/                           # Experiment and pipeline configuration files
│   ├── default.yaml                   # Master default parameters
│   ├── train.yaml                     # Training hyperparameters
│   ├── evaluation.yaml                # Evaluation parameters
│   ├── inference.yaml                 # Inference settings
│   └── data_generation.yaml           # Synthetic data generation settings
│
├── multimodal_malware/                # Core Python package
│   ├── features/                      # Multimodal feature extractors (Opcode, CFG, Syscall)
│   ├── models/                        # Neural network architectures & losses
│   ├── training/                      # Dataset loaders, batch collators, training routines
│   ├── evaluation/                    # Metrics, sweepers, and benchmarking routines
│   ├── sandbox/                       # Dynamic tracing and sandbox utilities
│   ├── similarity/                    # Vector similarity indexing and retrieval
│   ├── scripts/                       # CLI tools (train, evaluate, inference, benchmark)
│   ├── pages/                         # Streamlit UI workbench pages
│   └── app.py                         # Streamlit application entry point
│
├── scripts/ -> multimodal_malware/scripts  # Convenience symlink for CLI execution
│   ├── generate_data.py               # Deterministic benchmark shard generator
│   ├── train.py                       # Model training CLI
│   ├── evaluate.py                    # Evaluation CLI (nominal, temporal, holdout)
│   ├── inference.py                   # Single-sample / batch inference CLI
│   └── benchmark.py                   # Execution latency profiler
│
├── datasets/                          # Dataset manifests, shards, and evaluation splits
│   ├── README.md                      # Dataset provenance and layout documentation
│   ├── manifests/                     # 100K corpus catalog manifest
│   ├── benchmark_100k/                # 10 materialized shards (10,000 samples)
│   ├── train_split.pt                 # Training partition (7,000 samples)
│   ├── val_split.pt                   # Validation partition (1,500 samples)
│   ├── test_split.pt                  # Nominal test partition (1,500 samples)
│   └── seed_disjoint_test_split.pt    # Generator-seed-disjoint OOD partition (1,500 samples)
│
├── checkpoints/                       # Trained PyTorch model artifacts
│   ├── README.md                      # Checkpoint metadata and training history
│   ├── best_model.pt                  # Best validation checkpoint (7.26 MB)
│   ├── latest_model.pt                # Terminal training checkpoint (7.26 MB)
│   ├── model_manifest.json            # Architecture parameters and tensor shapes
│   └── training_history.json          # Epoch-by-epoch training logs
│
├── results/                           # Experimental metrics, tables, and benchmarks
│   ├── README.md                      # Experimental output directory guide
│   ├── metrics/                       # Machine-readable metric JSON/CSV artifacts
│   ├── tables/                        # Formatted CSV evaluation tables
│   ├── figures/                       # Analytical vector PDFs and 300-DPI PNGs
│   ├── benchmarks/                    # Hardware latency logs
│   ├── logs/                          # Forensic audits and verification reports
│   ├── raw_eval_artifacts.npz         # Raw evaluation tensors (y_true, y_pred, y_prob)
│   └── FINAL_RESULTS.csv              # Master results table across all experimental models
│
├── docs/                              # Project documentation
│   ├── installation.md                # Environment setup guide
│   ├── usage.md                       # CLI and interactive workflow guide
│   ├── reproducibility.md             # Reproduction instructions
│   ├── data.md                        # Dataset and feature representation guide
│   ├── architecture.md                # Neural network architecture & equations
│   └── result_verification.md         # Claim-to-artifact verification matrix
│
└── tests/ -> multimodal_malware/tests # Automated test suite (68 passing tests)
```

---

## Requirements

- **Operating System:** Linux or macOS
- **Python:** $\ge$ 3.9 (Tested on Python 3.14.7)
- **PyTorch:** $\ge$ 2.2.0 (Tested on PyTorch 2.14.0)
- **Key Libraries:** `torch-geometric`, `capstone`, `lief`, `scikit-learn`, `pandas`, `plotly`, `streamlit`, `pytest`

---

## Installation

```bash
# 1. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Upgrade packaging tools
pip install --upgrade pip setuptools wheel

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) Install package in development mode
pip install -e .
```

Verify the installation by running the test suite:

```bash
pytest tests
```

---

## Data

The repository provides:
- **Included:** 100,000-sample catalog manifest (`datasets/manifests/dataset_manifest.jsonl`), 10 materialized multimodal feature shards (10,000 samples across `datasets/benchmark_100k/shards/`), and frozen deterministic partitions (`train_split.pt`, `val_split.pt`, `test_split.pt`, `seed_disjoint_test_split.pt`).
- **Reproducible Generation:** Shards can be deterministically regenerated from scratch using:
  ```bash
  python scripts/generate_data.py --num-shards 10 --samples-per-shard 1000 --seed 42 --output-dir datasets/benchmark_100k
  ```
- **Provenance & Integrity:** Partitions are strictly disjoint ($\text{Train} \cap \text{Val} = \emptyset$, $\text{Train} \cap \text{Test} = \emptyset$, $\text{Val} \cap \text{Test} = \emptyset$, zero hash collisions).
- Details and data schemas are documented in [docs/data.md](docs/data.md).

---

## Training

To train the complete tri-modal architecture:

```bash
python scripts/train.py --config configs/train.yaml
```

Checkpoints will be saved to `checkpoints/best_model.pt` and `checkpoints/latest_model.pt` along with epoch logs in `checkpoints/training_history.json`.

---

## Evaluation

To evaluate a trained checkpoint on the held-out test partition:

```bash
python scripts/evaluate.py --checkpoint checkpoints/best_model.pt --split test --output-dir results
```

To evaluate zero-day generalization on the quarantined WannaCry family:

```bash
python scripts/evaluate.py --checkpoint checkpoints/best_model.pt --split family_holdout --output-dir results
```

To evaluate chronological robustness across simulated quarters:

```bash
python scripts/evaluate.py --checkpoint checkpoints/best_model.pt --split temporal --output-dir results
```

---

## Inference

Run inference on single binary samples or synthetic instances:

```bash
# Run inference on a generated synthetic test sample
python scripts/inference.py --checkpoint checkpoints/best_model.pt --synthetic

# Run inference on a specific sample from the test split
python scripts/inference.py --checkpoint checkpoints/best_model.pt --sample-index 5

# Output machine-readable JSON
python scripts/inference.py --checkpoint checkpoints/best_model.pt --sample-index 5 --json
```

Output includes predicted class (`BENIGN` or `MALWARE`), probability score $P(\text{Malware})$, modality attention allocation ($\alpha_{\text{opcode}}, \alpha_{\text{cfg}}, \alpha_{\text{syscall}}$), and triage escalation recommendation.

---

## Benchmarking

Measure latency across neural components and triage stages:

```bash
python scripts/benchmark.py --checkpoint checkpoints/best_model.pt --output results/benchmarks/latency_benchmark.json
```

Measured performance on a single CPU core:
- **Fast Static Triage (Stage 1):** 17.53 ms (86.2% sandbox escalation reduction)
- **Full Tri-Modal Forward Pass:** 28.87 ms (34.6 binaries/second)
- **Memory Footprint:** 512.5 MB RSS during peak inference

---

## Results

Key verified performance metrics on the nominal 1,500-sample test partition:

| Metric | Measured Value | 95% Confidence Interval |
|---|---|---|
| **Accuracy** | 99.73% (1,496 / 1,500) | [99.32%, 99.90%] (Wilson Score) |
| **Precision** | 100.00% (740 / 740) | [99.49%, 100.00%] |
| **Recall** | 99.46% (740 / 744) | [98.63%, 99.80%] |
| **F1-Score** | 0.9973 | [0.9946, 0.9993] (Bootstrap) |
| **Clean FPR** | 0.00% (0 / 756) | — |
| **Clean FNR** | 0.54% (4 / 744) | — |
| **ROC-AUC** | 1.0000 | — |
| **PR-AUC** | 1.0000 | — |
| **WannaCry Zero-Day Recall** | 100.00% (157 / 157) | Mean confidence: 0.9297 |
| **Seed-Disjoint OOD Accuracy** | 99.33% (1,490 / 1,500) | Macro F1: 0.9933 |

Detailed numerical results, ablation comparisons, and statistical tests are documented in [docs/result_verification.md](docs/result_verification.md) and [results/](results/).

---

## Reproducibility

For a complete step-by-step reproduction guide and one-click execution:

```bash
python reproduce_all.py
```

See [docs/reproducibility.md](docs/reproducibility.md) for detailed instructions.

---

## Interactive Workstation

Launch the interactive research workstation:

```bash
streamlit run app.py
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
