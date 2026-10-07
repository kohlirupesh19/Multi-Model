# Dataset Organization and Provenance

This directory contains the dataset manifests, materialized feature shards, deterministic partitions, and out-of-distribution (OOD) evaluation splits used by the multi-modal binary analysis platform.

## Directory Layout

```
datasets/
├── README.md                          # Dataset documentation and provenance guide
├── manifests/
│   └── dataset_manifest.jsonl         # 100,000-sample corpus catalog manifest
├── metadata/
│   └── dataset_summary.json           # Class distributions, family statistics, and split metadata
├── benchmark_100k/
│   ├── dataset_manifest.json          # Formatted JSON manifest (100,000 records)
│   ├── dataset_manifest.jsonl         # Streaming JSONL manifest (100,000 records)
│   ├── dataset_summary.json           # Partition summary and family breakdown
│   └── shards/                        # 10 materialized feature shards (1,000 samples each)
│       ├── shard_000.pt to shard_009.pt
├── train_split.pt.gz                  # Deterministic training partition (7,000 samples; gzipped; auto-extracted to .pt on load)
├── val_split.pt                       # Deterministic validation partition (1,500 samples; 50% benign, 50% malware)
├── test_split.pt                      # Nominal held-out test partition (1,500 samples: 756 benign, 744 malware)
└── seed_disjoint_test_split.pt        # Generator-seed-disjoint OOD partition (1,500 samples)
```

## Dataset Specifications

| Partition | Sample Count | Class Balance | Purpose |
|---|---|---|---|
| **Catalog Manifest** | 100,000 binaries | 50.0% Benign / 50.0% Malware | Corpus indexing and metadata catalog |
| **Materialized Cohort** | 10,000 binaries | 50.0% Benign / 50.0% Malware | Extracted tri-modal tensor representation across 10 deterministic shards |
| **Training Split** (`train_split.pt` / `train_split.pt.gz`) | 7,000 binaries | 3,500 Benign / 3,500 Malware | Representation learning & classifier optimization |
| **Validation Split** (`val_split.pt`) | 1,500 binaries | 750 Benign / 750 Malware | Hyperparameter tuning and checkpoint selection |
| **Nominal Test Split** (`test_split.pt`) | 1,500 binaries | 756 Benign / 744 Malware | Final unbiased performance assessment |
| **Seed-Disjoint OOD** (`seed_disjoint_test_split.pt`) | 1,500 binaries | 750 Benign / 750 Malware | Verification against synthetic generator bias |
| **Held-Out Family** | 157 binaries | 100% WannaCry Ransomware | Zero-day family generalization stress test |

## Provenance and Leakage Auditing

1. **SHA-256 Disjointness**:
   - `Train ∩ Val` = $\emptyset$ (0 hashes)
   - `Train ∩ Test` = $\emptyset$ (0 hashes)
   - `Val ∩ Test` = $\emptyset$ (0 hashes)
2. **Preprocessing Isolation**:
   - Feature extractors, opcode tokenizers, and normalization parameters use fixed global vocabularies configured strictly prior to inference without test partition leakage.
3. **Zero-Day Holdout Protocol**:
   - The entire `ransomware_wannacry` family (157 instances) is completely quarantined from the training and validation partitions.

## Synthetic Data Generation

To regenerate the materialized shards from scratch deterministically:

```bash
# Generate 10 shards (10,000 samples total) with seed 42
python scripts/generate_data.py --num-shards 10 --samples-per-shard 1000 --seed 42 --output-dir datasets/benchmark_100k
```

Or using the standard dataset builder:

```bash
python scripts/generate_dataset.py
```
