# Precomputed Feature Cache

This directory stores intermediate precomputed multi-modal feature representations to avoid redundant disassembler and CFG extraction overhead during benchmarking.

## Structure

- **[`features_index.sqlite`](./features_index.sqlite)**: SQLite index mapping SHA-256 sample hashes to feature metadata, extraction timestamps, and tensor file pointers.
- **`tensors/`**: Individual serialized PyTorch tensor representations (`.pt`) for opcode tokens, CFG edge lists, and syscall n-gram vectors.
