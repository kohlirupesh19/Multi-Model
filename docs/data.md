# Dataset Specifications and Feature Extraction

This document outlines the multi-modal dataset pipeline, tensor representations, feature extractors, and split partitioning protocols.

---

## 1. Multimodal Feature Representations

The framework consumes three distinct execution modalities per binary sample:

### 1.1 Opcode Sequence Stream (`opcode_tensor`)
- **Extraction Tool:** Capstone Disassembly Engine
- **Input Representation:** Linear disassembly stream filtered for mnemonic tokens.
- **Vocabulary Size:** 4,096 tokens (mapped to frequent x86/x64 instruction mnemonics and addressing forms).
- **Sequence Length:** Truncated / padded to 2,048 tokens using importance-weighted head-tail sampling.
- **Tensor Shape:** `(B, 2048)` of `torch.int64`.

### 1.2 Control Flow Graph Stream (`cfg_data`)
- **Extraction Tool:** Static Basic-Block CFG Builder (via `multimodal_malware/features/cfg_extractor.py`)
- **Graph Representation:** Directed graph $\mathcal{G} = (\mathcal{V}, \mathcal{E})$ where vertices represent basic blocks and edges represent branch, jump, and fallthrough control transitions.
- **Node Features:** 16-dimensional continuous feature vectors capturing instruction mix, block length, entropy, and cyclomatic complexity.
- **Hub Preservation:** Hub-preserving topology compression ensuring maximum graph size $\le 1,000$ vertices and $\le 3,000$ edges.
- **Tensor Structure:** PyTorch Geometric `Data` or `Batch` object containing `x` (node features) and `edge_index` (connectivity pairs).

### 1.3 System Call Sequence Stream (`syscall_tensor`)
- **Extraction Mechanism:** Dynamic API execution monitoring / simulated sandbox telemetry.
- **Canonical Vocabulary:** 128 standard Windows / POSIX system calls (file I/O, registry modifications, process injection, network sockets).
- **Sequence Length:** Fixed trace window of 512 chronological invocations.
- **Tensor Shape:** `(B, 512)` of `torch.int64`.
- **Availability Mask:** Boolean flag `has_syscall` indicating whether dynamic behavioral tracing successfully completed or timed out / stalled due to anti-analysis defense.

---

## 2. Benchmark Corpus Organization

The repository provides both metadata manifests and pre-materialized feature tensors:

- **100,000 Catalog Manifest (`datasets/manifests/dataset_manifest.jsonl`):**
  Each line contains JSON metadata:
  ```json
  {
    "sha256": "3a7b9c...",
    "label": 1,
    "family": "ransomware_wannacry",
    "timestamp": 1680123456,
    "size_bytes": 1048576,
    "has_syscall": true
  }
  ```
- **10 Materialized Shards (`datasets/benchmark_100k/shards/`):**
  Files `shard_000.pt` through `shard_009.pt`, each packaging 1,000 multimodal dictionaries.

---

## 3. Partitioning and Leakage Guarantees

The 10,000 materialized samples are partitioned into frozen splits:

- **`train_split.pt` (7,000 samples):** 3,500 Benign, 3,500 Malware.
- **`val_split.pt` (1,500 samples):** 750 Benign, 750 Malware.
- **`test_split.pt` (1,500 samples):** 756 Benign, 744 Malware.

### Split Disjointness Verification
- $\text{Train} \cap \text{Val} = \emptyset$
- $\text{Train} \cap \text{Test} = \emptyset$
- $\text{Val} \cap \text{Test} = \emptyset$
- Zero SHA-256 hash collision between any partition pair.
- The single-family holdout `ransomware_wannacry` is strictly absent from `train_split.pt` and `val_split.pt`.

---

## 4. Deterministic Data Generation

To regenerate feature tensors from synthetic distributions:

```bash
python scripts/generate_data.py \
    --num-shards 10 \
    --samples-per-shard 1000 \
    --seed 42 \
    --output-dir datasets/benchmark_100k
```
