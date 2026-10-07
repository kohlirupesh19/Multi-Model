# Installation and Environment Setup

This document describes how to set up the multi-modal malware detection project on Linux and macOS environments.

## System Prerequisites

- **Python**: Version 3.9 through 3.14 supported (Tested on Python 3.14.7)
- **PyTorch**: Version 2.2.0 or newer (Tested on PyTorch 2.14.0)
- **RAM**: Minimum 8 GB recommended (Evaluation requires < 550 MB RSS)
- **Hardware Acceleration**: CPU-standardized; supports Apple Silicon (Metal Performance Shaders / MPS) and NVIDIA CUDA when available.

## Standard Virtual Environment Installation

```bash
# 1. Clone or navigate to the repository root
cd Multi-Model

# 2. Create and activate a clean virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Upgrade pip, wheel, and setuptools
pip install --upgrade pip setuptools wheel

# 4. Install production dependencies
pip install -r requirements.txt

# 5. (Optional) Install the project in editable development mode
pip install -e .
```

## Conda Environment Installation (Alternative)

If using Anaconda or Miniconda:

```bash
# Create environment from provided environment.yml
conda env create -f environment.yml

# Activate the environment
conda activate multimodal-malware
```

## Verifying the Installation

To verify that all dependencies and core neural modules load correctly:

```bash
# Run the automated pytest suite (68 tests)
pytest tests

# Verify model loading and inference CLI smoke test
python scripts/inference.py --checkpoint checkpoints/best_model.pt --synthetic
```
