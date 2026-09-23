# Benchmark Datasets

This directory contains the dataset manifests, materialized sample shards, and frozen evaluation splits for the benchmark.

## Dataset Structure

```
datasets/
├── README.md                  # This documentation
├── test_split.pt              # Frozen PyTorch evaluation test split (1,500 samples: 756 benign, 744 malware)
├── benchmark_100k/            # Full 100k-sample corpus metadata & materialized shards
│   ├── dataset_manifest.json  # Complete 100k-sample metadata manifest
│   ├── dataset_manifest.jsonl # JSONL formatted 100k-sample metadata manifest
│   ├── dataset_summary.json   # Distribution statistics, family counts, and hash registers
│   └── shards/                # 10 materialized shards (10,000 multimodal feature samples)
└── benchmark_subset/          # Quick sanity benchmark metadata subset
    └── dataset_manifest.json
```

## Partitioning

- **Total Corpus Manifest:** 100,000 samples
- **Materialized Benchmark Shards:** 10 shards × 1,000 samples = 10,000 samples
- **Partition Splits:**
  - Training: 7,000 samples (70%)
  - Validation: 1,500 samples (15%)
  - Testing: 1,500 samples (15%) (`test_split.pt`)
- **Held-Out Family Protocol:** 157 sample-level WannaCry test samples completely excluded from training.
