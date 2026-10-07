# Project Usage Guide

This guide details the primary command-line and interactive interfaces available in the project.

---

## 1. Data Generation

To synthesize or materialize multimodal feature tensors into deterministic shards:

```bash
# Generate 10 deterministic shards (10,000 samples)
python scripts/generate_data.py --num-shards 10 --samples-per-shard 1000 --seed 42 --output-dir datasets/benchmark_100k

# Generate train, val, and test frozen splits
python scripts/generate_dataset.py
```

---

## 2. Model Training

Train the tri-modal architecture with Opcode Transformer, CFG-GIN, Syscall-BiLSTM, InfoNCE hyperspherical alignment, and Volumetric GRAM loss:

```bash
# Run training with default configuration
python scripts/train.py --config configs/train.yaml

# Train with specific epochs and batch size
python scripts/train.py --epochs 10 --batch-size 32 --lr 1e-4 --output-dir checkpoints
```

Artifacts generated:
- `checkpoints/best_model.pt`: Checkpoint achieving highest validation F1 score.
- `checkpoints/latest_model.pt`: Model state at final training epoch.
- `checkpoints/training_history.json`: Epoch logs and learning curves.

---

## 3. Evaluation

Evaluate model checkpoints across test splits, chronological partitions, or held-out malware families:

```bash
# Nominal held-out test split evaluation (1,500 samples)
python scripts/evaluate.py --checkpoint checkpoints/best_model.pt --split test --output-dir results

# Temporal drift evaluation across chronological quarters
python scripts/evaluate.py --checkpoint checkpoints/best_model.pt --split temporal --output-dir results

# Zero-day single-family holdout evaluation (WannaCry)
python scripts/evaluate.py --checkpoint checkpoints/best_model.pt --split family_holdout --output-dir results
```

---

## 4. Inference

Perform real-time tri-modal inference on single binary samples or synthetic instances:

```bash
# Run inference on a generated synthetic sample
python scripts/inference.py --checkpoint checkpoints/best_model.pt --synthetic

# Run inference on a specific sample from the test split
python scripts/inference.py --checkpoint checkpoints/best_model.pt --sample-index 5

# Output machine-readable JSON decision
python scripts/inference.py --checkpoint checkpoints/best_model.pt --sample-index 5 --json
```

Output includes:
- Predicted class (`BENIGN` or `MALWARE`)
- Probability score $P(\text{Malware})$
- Modality attention allocation ($\alpha_{\text{opcode}}, \alpha_{\text{cfg}}, \alpha_{\text{syscall}}$)
- Triage stage escalation recommendation (`STATIC_RESOLUTION` vs. `DYNAMIC_SANDBOX_ESCALATION`)

---

## 5. Latency and Hardware Benchmarking

Measure per-component feature extraction and neural forward pass execution times:

```bash
python scripts/benchmark.py --checkpoint checkpoints/best_model.pt --output results/benchmarks/latency_benchmark.json
```

---

## 6. Interactive Research Dashboard

Launch the Streamlit research workstation UI:

```bash
streamlit run app.py
```

The interactive workstation provides:
- Single-binary inspection and modality visualizer
- Decision threshold sweep explorer
- Obfuscation and evasion robustness stress test
- Nearest-neighbor binary similarity search
