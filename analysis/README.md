# Analytical Figure Generation & Verification

This directory contains the Python scripts and generated vector/raster outputs for all publication figures in the revised manuscript.

## Directory Structure

```
analysis/
└── figures/
    ├── common_style.py                  # Typography, font configuration, and color palettes
    ├── generate_all_figures.py          # Master runner for all figure generators
    ├── generate_*.py                    # Individual figure generation scripts (18 scripts)
    └── output/                          # Verified output figures (PDF + 300-DPI PNG)
        ├── Fig_01_Dataset_Flow.{pdf,png}
        ├── Fig_03_Benchmark_Comparison.{pdf,png}
        ├── Fig_04_Confusion_Matrix.{pdf,png}
        ├── Fig_05_ROC_Curves.{pdf,png}
        ├── Fig_06_PR_Curves.{pdf,png}
        ├── Fig_07_Modality_Ablation.{pdf,png}
        ├── Fig_13_Robustness_Analysis.{pdf,png}
        ├── Fig_15_WannaCry_Holdout.{pdf,png}
        ├── Fig_16_Latency_Breakdown.{pdf,png}
        ├── Fig_17_Latency_vs_F1.{pdf,png}
        └── Fig_18_Embedding_Visualization.{pdf,png}
```

## Regeneration

To regenerate all analytical figures directly from verified experimental outputs:
```bash
python analysis/figures/generate_all_figures.py
```
