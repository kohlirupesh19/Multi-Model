# Experiment Configurations

This directory contains YAML configuration files defining model hyperparameters, training settings, and experimental scaling regimes.

## Configuration Profiles

| File | Purpose | Key Parameters |
|---|---|---|
| [`full_multimodal.yaml`](./full_multimodal.yaml) | Standard Tri-Modal Architecture (Opcode + CFG + Syscall) | Embedding dim: 256, Fusion: Cross-Attention, Volumetric GRAM Loss |
| [`high_accuracy.yaml`](./high_accuracy.yaml) | High-Accuracy Production Configuration | Optimized learning rate (1e-4), cosine decay, 50 epochs |
| [`contrastive.yaml`](./contrastive.yaml) | Pure Self-Supervised Contrastive Pretraining | InfoNCE loss, temperature tau=0.07, batch size 64 |
| [`lightweight.yaml`](./lightweight.yaml) | Edge/Resource-Constrained Configuration | 128-dim embeddings, pruned CFG GIN, CPU inference latency <15 ms |
| [`scale_100k.yaml`](./scale_100k.yaml) | Large-Scale Distributed Sharding Configuration | 100k-sample streaming loader, dynamic shard prefetching |
