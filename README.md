# Tri-Modal Contrastive Binary Analysis: Systematic Review and Reproducible Benchmark

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Framework: PyTorch](https://img.shields.io/badge/PyTorch-2.2+-ee4c2c.svg)](https://pytorch.org/)
[![PyG](https://img.shields.io/badge/PyG-2.5+-3C2179.svg)](https://pyg.org/)
[![Tests: 40/40 Passing](https://img.shields.io/badge/tests-40%2F40%20passing-brightgreen.svg)](tests/)
[![Springer Nature](https://img.shields.io/badge/Springer-sn--jnl-blueviolet.svg)](Research%20Paper/revised_manuscript/)

Official open-source repository and reproducibility benchmark for the scientific manuscript:  
**"Tri-Modal Contrastive Binary Analysis via Opcode Transformers, Control Flow Graph Isomorphism Networks, and System Call Embeddings: A Systematic Review and Reproducible Benchmark"**

---

## 🧭 Reviewer Quick Navigation Guide

For peer reviewers and editors auditing the revised manuscript, all primary artifacts, verification spreadsheets, and audit trails are structured in dedicated directories:

| Deliverable | Location | Description |
| :--- | :--- | :--- |
| 📄 **Final Revised Manuscript (PDF)** | [`Research Paper/FINAL_REVISED_MANUSCRIPT.pdf`](Research%20Paper/FINAL_REVISED_MANUSCRIPT.pdf) | Official 27-page compiled Springer Nature PDF with all 14 figures and 10 tables. |
| 📝 **Point-by-Point Response** | [`Research Paper/POINT_BY_POINT_REVIEWER_RESPONSE.docx`](Research%20Paper/POINT_BY_POINT_REVIEWER_RESPONSE.docx) | Comprehensive point-by-point response letter addressing all reviewer comments. |
| 📊 **Master Verification Workbook** | [`Research Paper/verification_excel/MASTER_VERIFICATION_AUDIT.xlsx`](Research%20Paper/verification_excel/MASTER_VERIFICATION_AUDIT.xlsx) | Cell-by-cell claim provenance, compliance matrix, and raw metric reconciliation. |
| 📑 **LaTeX Source Code** | [`Research Paper/revised_manuscript/sn-article.tex`](Research%20Paper/revised_manuscript/sn-article.tex) | Complete TeX source, bibliography (`sn-bibliography.bib`), and template classes. |
| 🧪 **Single Source of Truth Results** | [`Research Paper/FINAL_RESULTS.csv`](Research%20Paper/FINAL_RESULTS.csv) | Verified canonical benchmark metrics across all 22 experimental configurations. |
| 📈 **Analytical Figures (PDF/PNG)** | [`analysis/figures/output/`](analysis/figures/output/) | Publication-quality 300-DPI PNG and vector PDF figures generated from raw logs. |

---

## ⚡ 1-Click Verification & Reproduction Commands

All benchmark results can be reproduced directly on a standard CPU/workstation without external cluster dependencies:

### 1. Independent Metric Verification (Phase 6 Audit)
Loads the model checkpoint and held-out test split, computes forward predictions on all 1,500 test samples, and recalculates Wilson score and bootstrap confidence intervals:
```bash
python INDEPENDENT_METRIC_VERIFICATION.py
```
*Expected output: Accuracy = 99.7333%, Precision = 100.00%, Recall = 99.4624%, F1 = 0.9973, WannaCry Recall = 100.0%.*

### 2. Execute Automated Integrity Test Suite (40 Tests)
Runs the complete test suite verifying mathematical consistency, split disjointness, confusion matrix arithmetic, and sensitivity sweeps:
```bash
pytest tests/
```
*Status: All 40 unit and integration tests pass cleanly in under 5 seconds.*

### 3. Recompile the Springer Manuscript
Compiles the master LaTeX document into publication-ready PDF:
```bash
tectonic "Research Paper/revised_manuscript/sn-article.tex"
```

### 4. Regenerate Publication Figures
Regenerates all 11 active manuscript figures into vector PDF and 300-DPI PNG formats:
```bash
python -m analysis.figures.generate_all_figures
```

### 5. Launch Interactive Streamlit Research Dashboard
Launches the interactive research platform with model inspection, live inference, and similarity search:
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser.

---

## 📊 Verified Empirical Benchmark Summary

The proposed tri-modal framework combines an **Opcode Transformer**, a **Control Flow Graph Isomorphism Network (GIN)**, and a **Dynamic Syscall Bi-LSTM** aligned via multi-channel **InfoNCE** and **Volumetric Gramian (GRAM)** regularization with adaptive attention fusion.

| Metric | Verified Empirical Value | Verification Ground Truth |
| :--- | :--- | :--- |
| **Test Accuracy** | **99.73%** (1,496 / 1,500 samples) | Wilson 95% CI: $[99.32\%, 99.90\%]$; Bootstrap CI: $[99.47\%, 99.93\%]$ |
| **Precision** | **100.00%** (0 False Positives) | Specificity = $100.0\%$ (756 / 756 Benign) |
| **Recall (Sensitivity)** | **99.46%** (4 False Negatives) | Sensitivity = $99.46\%$ (740 / 744 Malware) |
| **Macro F1-Score** | **0.9973** | Non-overlapping CIs vs. all baseline models ($\le 0.9120$) |
| **ROC-AUC / PR-AUC** | **1.000 / 0.9997** | Area under ROC and Precision-Recall curves |
| **Zero-Day WannaCry Holdout** | **100.0% Detection** (157 / 157 samples) | Mean prediction confidence = $0.9297$; 0 False Negatives |
| **UPX Obfuscation Robustness** | **88.0% Accuracy** (FPR = 24.0%) | Attention dynamically shifts to syscalls ($\alpha_{\text{sys}} = 0.343$) |
| **Full Forward Latency** | **28.87 ms** (CPU Architecture) | Opcode: 16.44 ms; GIN: 0.86 ms; Syscall: 11.05 ms; Fusion: 0.09 ms |
| **Fast Static Triage Latency** | **17.53 ms** (57.0 samples/sec) | **86.2%** of binaries resolved statically; avoids sandbox queue delays |
| **Total Neural Parameters** | **994,178 parameters** | Fast Static Triage sub-network: 778,370 parameters |

---

## 📁 Repository Directory Architecture

```text
Multi-Model/
├── INDEPENDENT_METRIC_VERIFICATION.py  # 1-click authoritative metric verification CLI
├── app.py                              # Interactive Streamlit dashboard entry point
├── pages/                              # Streamlit analytical modules and inspection views
├── README.md                           # Master repository guide and reviewer roadmap
├── requirements.txt                    # Python runtime package dependencies
├── environment.yml                     # Conda virtual environment specification
├── pytest.ini                          # Automated test discovery and warning filters
│
├── Research Paper/                     # Scientific manuscript and reviewer audit packages
│   ├── FINAL_REVISED_MANUSCRIPT.pdf    # Official compiled Springer submission PDF (27 pages)
│   ├── FINAL_REVISED_MANUSCRIPT.docx   # Formatted Word document for editorial workflows
│   ├── POINT_BY_POINT_REVIEWER_RESPONSE.docx # Official point-by-point reviewer response
│   ├── FINAL_RESULTS.csv               # Single source of truth benchmark results (22 experiments)
│   ├── revised_manuscript/             # Springer Nature LaTeX sources, bibtex, and figures
│   │   ├── sn-article.tex              # Master LaTeX manuscript source file
│   │   ├── sn-bibliography.bib         # Verified bibliography (31 peer-reviewed citations)
│   │   ├── sn-jnl.cls                  # Official Springer Nature document class
│   │   └── figures/                    # 14 publication figures embedded in manuscript
│   ├── verification_excel/             # Official audit workbooks for reviewer inspection
│   │   ├── MASTER_VERIFICATION_AUDIT.xlsx      # Master consolidated audit workbook
│   │   ├── CLAIM_PROVENANCE_MATRIX.xlsx        # Claim-to-file provenance mapping
│   │   ├── REVIEWER_COMPLIANCE_MATRIX.xlsx     # Compliance tracking across all comments
│   │   ├── DATASET_AND_SPLIT_AUDIT.xlsx        # Dataset materialization and partition audit
│   │   ├── FINAL_RESULTS_BENCHMARK.xlsx        # Authoritative metric verification tables
│   │   ├── DOI_AND_LITERATURE_AUDIT.xlsx       # PRISMA literature and DOI audits
│   │   ├── EXPERIMENT_AND_RQ_PROVENANCE.xlsx   # RQ evidence and hypothesis reconciliation
│   │   └── FINAL_REFERENCE_AUDIT.xlsx          # 100% peer-reviewed citation audit
│   ├── response_to_reviewers/          # Markdown response letters and generation scripts
│   ├── audit/                          # Audit scripts, reports, and claim matrices
│   │   ├── reports/                    # 35 structured audit reports and CSV matrices
│   │   ├── scripts/                    # Reproducible audit generation scripts
│   │   └── AUDIT_SPECIFICATION_PROMPT.md # Comprehensive multi-phase audit prompt
│   └── original_manuscript/            # Pre-revision manuscript archive for comparison
│
├── multimodal_malware/                 # Core Python package & neural modules
│   ├── models/                         # Opcode Transformer, CFG-GIN, Syscall Bi-LSTM, GRAM, Fusion
│   ├── features/                       # PE/ELF parsing, Capstone disassembly, angr CFG, SQLite cache
│   ├── training/                       # Dataset loaders, stratified samplers, multi-task trainer
│   ├── evaluation/                     # Metric calculations, bootstrap CIs, threshold optimization
│   ├── similarity/                     # Vector similarity index & nearest-neighbor search
│   ├── sandbox/                        # Instrumented Cuckoo Sandbox trace parsing
│   ├── configs/                        # Declarative training and evaluation YAML configs
│   └── scripts/                        # Training, evaluation, and benchmark execution scripts
│
├── analysis/                           # Scientific figure generation and Pareto analysis
│   └── figures/                        # Matplotlib scripts adhering to Springer guidelines
│       └── output/                     # 11 active manuscript figures (vector PDF & 300-DPI PNG)
│
├── checkpoints/                        # Model weights, training logs, and manifests
│   ├── best_model.pt                   # Optimal trained model checkpoint weights
│   ├── model_manifest.json             # Model architecture hyperparameters and metadata
│   └── training_history.json           # Epoch-by-epoch loss convergence and metric history
│
├── datasets/                           # Dataset manifests and materialized evaluation shards
│   ├── benchmark_100k/                 # 100,000 executable binary manifest metadata
│   ├── benchmark_subset/               # Materialized sample tensors across subfamilies
│   └── test_split.pt                   # Verified 1,500 held-out test split tensors
│
├── results/                            # Raw empirical outputs and evaluation logs
│   ├── raw_eval_artifacts.npz          # Raw test predictions, labels, and 2D t-SNE embeddings
│   ├── evaluation_test.json            # Authoritative test metrics and 95% bootstrap CIs
│   ├── evaluation_family_holdout.json  # 157 WannaCry holdout predictions and recall
│   ├── evaluation_temporal.json        # Chronological temporal partition evaluation
│   ├── robustness_results.json         # Adversarial robustness under 4 attack transformations and clean baseline
│   ├── latency_benchmark.json          # Wall-clock CPU latency decomposition
│   ├── roc_curves.csv                  # Exact coordinate points for ROC curves
│   └── pr_curves.csv                   # Exact coordinate points for Precision-Recall curves
│
├── configs/                            # Declarative training and evaluation YAML configs
│   ├── full_multimodal.yaml            # Standard tri-modal architecture config
│   ├── high_accuracy.yaml              # Evaluated high-accuracy training config
│   ├── contrastive.yaml                # Pure InfoNCE self-supervised pretraining
│   ├── lightweight.yaml                # Low-latency evaluated edge configuration
│   └── scale_100k.yaml                 # 100k distributed sharding configuration
│
├── features_cache/                     # Precomputed feature cache & SQLite registry
│   ├── features_index.sqlite           # SQLite index mapping sample hashes to features
│   └── tensors/                        # Serialized tensor cache for opcode, CFG, and syscalls
│
├── presentation/                       # Project presentation slide deck
│   └── Multi_Modal_Malware_Analysis_Project_Presentation.pptx # Widescreen presentation deck
│
└── tests/                              # Comprehensive automated test suite (40 tests)
    ├── test_benchmark_integrity.py     # Confusion matrix and metric definition assertions
    ├── test_figure_integrity.py        # Mathematical reconciliation of figures with raw logs
    ├── test_dataset_scaling.py         # Sharded dataset collator and splitting checks
    ├── test_evaluation.py              # Metric calculation and confidence interval tests
    ├── test_features.py                # Opcode, CFG, and system call extraction unit tests
    ├── test_models.py                  # PyTorch forward-pass shapes and loss functions
    └── test_similarity.py              # Vector index retrieval and pairwise comparator tests
```

---

## 🛠️ Environment Setup & Installation

### Option 1: Standard Virtual Environment (Recommended)
```bash
# Clone the repository
git clone https://github.com/kohlirupesh19/Multi-Model.git
cd Multi-Model

# Create and activate Python virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install required dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Option 2: Conda Environment
```bash
conda env create -f environment.yml
conda activate multimodal_malware
```

---

## 📜 Scientific Citation & Authors

If you use this codebase or benchmark in your research, please cite the accompanying publication:

```bibtex
@article{Bhabad2026TriModal,
  author    = {Bhabad, Harish Parshuram and Patel, Atmeshkumar Subhashbhai and Rakhade, Vijay M. and Kohli, Rupesh and Patel, Nandini S.},
  title     = {Tri-Modal Contrastive Binary Analysis via Opcode Transformers, Control Flow Graph Isomorphism Networks, and System Call Embeddings: A Systematic Review and Reproducible Benchmark},
  journal   = {Springer Nature Journal of Computer Virology and Hacking Techniques},
  year      = {2026},
  url       = {https://github.com/kohlirupesh19/Multi-Model}
}
```
