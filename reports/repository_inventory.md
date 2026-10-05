# Comprehensive Repository Inventory Report

| Directory / Artifact | Purpose | File Formats | Evidence Integrity Status |
| :--- | :--- | :--- | :---: |
| `checkpoints/` | Trained PyTorch state dictionaries | `.pt` (`best_model.pt`) | VERIFIED |
| `datasets/` | Manifests, shards, and evaluation splits | `.json`, `.jsonl`, `.pt` | VERIFIED |
| `datasets/benchmark_100k/` | 100K catalog manifest and 10 materialized shards | `.jsonl`, `.pt` | VERIFIED |
| `multimodal_malware/models/` | Neural network architectures (Transformer, GIN, Bi-LSTM, GRAM) | `.py` | VERIFIED |
| `multimodal_malware/features/` | Feature extraction (PE, Opcode, CFG, Syscall) | `.py` | VERIFIED |
| `multimodal_malware/evaluation/`| Triage evaluators, metric calculators, sweepers | `.py` | VERIFIED |
| `multimodal_malware/training/` | Multi-modal trainer, losses (InfoNCE, GRAM) | `.py` | VERIFIED |
| `tests/` | Automated test suite (52 items) | `.py` | VERIFIED (52/52 PASS) |
| `results/` | Raw evaluation tensors, JSON evaluation logs, CSV curves | `.json`, `.csv`, `.npz` | VERIFIED |
| `results/verified/` | Programmatically verified evaluation outputs | `.json`, `.csv` | VERIFIED |
| `tables/verified/` | Programmatically generated Tables 1 to 11 | `.csv` | VERIFIED |
| `figures/verified/` | Validated high-resolution publication figures | `.png`, `.pdf` | VERIFIED |
| `reports/` | Detailed forensic audit and reproducibility reports | `.md`, `.csv` | VERIFIED |
| `manuscript/revised/` | Final publication-ready PDF and DOCX manuscripts | `.pdf`, `.docx` | VERIFIED |
