# Dataset Provenance and Forensic Audit

- **Manifest Catalog Size:** 100,000 binary records (`dataset_manifest.jsonl`)
- **Materialized Multimodal Cohort:** Exactly 10,000 instances across 10 deterministic shards
- **Training Partition:** 7000 samples (50.0% Benign, 50.0% Malware)
- **Validation Partition:** 1500 samples (50.0% Benign, 50.0% Malware)
- **Held-Out Test Partition:** 1500 samples (756 Benign, 744 Malware)
- **SHA-256 Split Disjointness:** STRICTLY DISJOINT (Zero Leakage)
