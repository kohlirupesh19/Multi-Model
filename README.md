# Multi-Modal Binary Malware Analysis Research Platform

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Framework: PyTorch](https://img.shields.io/badge/PyTorch-2.2+-ee4c2c.svg)](https://pytorch.org/)
[![PyG](https://img.shields.io/badge/PyG-2.5+-3C2179.svg)](https://pyg.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B.svg)](https://streamlit.io/)

> **Academic Notice**: *This software is an experimental implementation inspired by the conceptual framework described in the accompanying systematic review:*  
> *"Multi-Modal Contrastive Binary Analysis via Opcode Transformers, Control Flow Graph Isomorphism Networks, and System Call Embeddings: A Systematic Review and Conceptual Framework"*  
> The conceptual architecture proposed in the review is synthesized from surveyed literature and was not experimentally validated by the authors of the survey. This platform serves as a reproducible, experimentally validated reference implementation designed to rigorously evaluate those concepts.

---

## 1. Research Motivation & Core Architecture

Modern malware variants routinely evade unimodal detection pipelines:
- **Static Opcode analysis** is blinded by UPX packing, instruction substitution, and dead-code insertion.
- **Control Flow Graph (CFG) analysis** degrades under control-flow flattening (OLLVM) and opaque predicate insertion.
- **Dynamic behavioral sandboxing** incurs high compute overhead (multi-minute delays per binary) and is prone to sandbox-stalling logic.

This platform implements the paper's **four-stage multi-modal pipeline**:

```text
                    INPUT BINARY (PE / ELF)
                               |
             +-----------------+-----------------+
             |                 |                 |
             v                 v                 v
        OPCODE STREAM      CFG GRAPH       DYNAMIC SYSCALL
      (Disassembly/LIEF)  (Basic Blocks)   (Isolated VM/Trace)
             |                 |                 |
             v                 v                 v
        Transformer           GIN             BiLSTM
             |                 |                 |
             v                 v                 v
         z_opcode            z_cfg           z_syscall
             |                 |                 |
             +-----------------+-----------------+
                               |
                               v
                     L2 NORMALIZATION
                               |
                               v
                     CONTRASTIVE ALIGNMENT
                     /                   \
            Pairwise InfoNCE        Volumetric GRAM
                     \                   /
                      \                 /
                       v               v
                     SHARED LATENT SPACE (d=128)
                               |
                               v
                  ATTENTION-WEIGHTED LATE FUSION
                  (Dynamic alpha_m + Gating Mask)
                               |
                   +-----------+-----------+
                   |                       |
                   v                       v
            CLASSIFICATION          SIMILARITY SEARCH
         (Malware / Benign /       (FAISS Nearest Neighbors,
          Family / Abstain)         Top-10 Cosine Matches)
```

---

## 2. Key Capabilities & Laptop-First Optimization

1. **Lightweight Deployment**: CPU-first inference, low memory profile (8–16 GB RAM), graph/sequence sampling safeguards, disk and SQLite caching.
2. **Two-Stage Triage**:
   - **Stage 1 (Fast Triage)**: Static PE/ELF parsing, Opcode Transformer, and CFG-GIN execute in milliseconds without spinning up a sandbox.
   - **Stage 2 (Deep Sandbox Analysis)**: Triggered only for low-confidence or suspicious binaries.
3. **Robustness to Missing Modalities**: Dynamic gating network applies availability masks ($m_{opcode}, m_{cfg}, m_{syscall}$) so corrupted or unavailable modalities do not derail classification.
4. **Non-Fabrication Scientific Integrity**: Metrics are only reported if computed from verified experimental runs. Unexecuted experiments display `"Not evaluated yet"`.
5. **Rigorous Security**: All uploaded samples are isolated in `quarantine/` with SHA-256 random hashes. The host system never directly executes untrusted binaries.

---

## 3. Installation

### Option A: Standard Virtual Environment (Recommended)
```bash
# Clone and enter workspace
cd /path/to/Multi-Model

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Option B: Conda Environment
```bash
conda env create -f environment.yml
conda activate multimodal_malware
```

---

## 4. Quick Start & CLI Workflows

### 1. Launch Streamlit Research Dashboard
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser.

### 2. Inspect Available Datasets
```bash
python scripts/download_datasets.py --list
```

### 3. Precompute Features
```bash
python scripts/precompute_features.py --dataset benchmark_subset --workers 4
```

### 4. Train the Multi-Modal Model
```bash
python scripts/train.py --config configs/lightweight.yaml
```

### 5. Evaluate on Test Splits
```bash
# Standard Random Split
python scripts/evaluate.py --checkpoint checkpoints/best_model.pt --split test

# Temporal Drift Split
python scripts/evaluate.py --checkpoint checkpoints/best_model.pt --split temporal

# Zero-Day / Family-Held-Out Split
python scripts/evaluate.py --checkpoint checkpoints/best_model.pt --split family_holdout
```

### 6. Run Latency & Hardware Benchmarks
```bash
python scripts/benchmark.py --checkpoint checkpoints/best_model.pt
```

### 7. Run Obfuscation Robustness Suite
```bash
python scripts/run_robustness.py --checkpoint checkpoints/best_model.pt
```

---

## 5. Directory Structure

```text
multimodal_malware/
├── app.py                         # Streamlit entry point
├── pages/                         # 10 Dedicated analytical pages
├── models/                        # Transformer, GIN, BiLSTM, InfoNCE, GRAM, Fusion
├── features/                      # LIEF PE/ELF parser, Capstone opcode, CFG builder, cache
├── sandbox/                       # Isolated VM abstraction & trace parsing
├── training/                      # Dataset, samplers, multi-stage trainer
├── evaluation/                    # Metrics, threshold sweep, zero-day, temporal, latency
├── similarity/                    # Vector index & nearest neighbor similarity
├── scripts/                       # Dataset downloader, feature precomputer, train/eval CLIs
├── configs/                       # Lightweight, contrastive, and full YAML configs
├── tests/                         # Full Pytest test suite
├── checkpoints/                   # Saved model state dicts & manifests
├── datasets/                      # Verified dataset repositories & metadata
├── features_cache/                # SQLite & disk feature caches
├── experiments/                   # Experiment tracking artifacts
└── quarantine/                    # Isolated upload staging directory
```

---

## 6. Scientific Integrity & Attribution

- **No Fabricated Benchmarks**: All metrics presented in the UI or CLI are generated from actual stored results in `experiments/` or calculated in real-time.
- **Reference Distinction**: Literature metrics cited from the systematic review are explicitly denoted with `[Literature Reference]` to avoid conflating prior surveyed papers with our local experimental prototype.
- **GRAM Regularization**: Volumetric GRAM is implemented as defined in Equation 10 of the paper:
  $$\mathcal{L}_{GRAM} = \frac{1}{N}\sum_{i=1}^N \det(G_i^+) - \lambda_{sep}\log(1 + \det(G_i^-))$$
  with numerical safeguards ($\det(G) + \epsilon I$).

---

## 7. License
This project is licensed under the [MIT License](LICENSE).
