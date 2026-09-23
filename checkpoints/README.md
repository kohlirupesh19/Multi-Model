# Model Checkpoints

This directory contains trained PyTorch model checkpoints and training logs for the Tri-Modal Malware Detection network.

## Checkpoint Files

| File | Size | Description |
|---|---|---|
| [`best_model.pt`](./best_model.pt) | 7.26 MB | Authoritative best checkpoint achieved during training (Epoch with lowest validation loss and highest F1-score: 0.9973) |
| [`latest_model.pt`](./latest_model.pt) | 7.26 MB | Final state checkpoint after training completion |
| [`model_manifest.json`](./model_manifest.json) | 391 B | Architecture metadata, parameter counts (1.89M parameters), and input tensor specifications |
| [`training_history.json`](./training_history.json) | 4.53 KB | Epoch-by-epoch training logs: loss, validation accuracy, F1-score, and learning rate curves |
