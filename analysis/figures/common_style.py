"""
Common Publication-Grade Styling Module for Springer Scientific Figures.
Ensures consistency in typography, color palette, axes, grids, and multi-format export (PDF + PNG).
"""

import os
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Directories
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = PROJECT_ROOT / "analysis" / "figures" / "output"
MANUSCRIPT_FIG_DIR = PROJECT_ROOT / "results" / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
MANUSCRIPT_FIG_DIR.mkdir(parents=True, exist_ok=True)

# Data paths
RESULTS_DIR = PROJECT_ROOT / "results"
RAW_ARTIFACTS_PATH = RESULTS_DIR / "raw_eval_artifacts.npz"
ROC_CSV_PATH = RESULTS_DIR / "roc_curves.csv"
PR_CSV_PATH = RESULTS_DIR / "pr_curves.csv"
INDEP_VERIF_JSON = RESULTS_DIR / "independent_verification_results.json"
TEST_EVAL_JSON = RESULTS_DIR / "evaluation_test.json"
TEMPORAL_EVAL_JSON = RESULTS_DIR / "evaluation_temporal.json"
FAMILY_EVAL_JSON = RESULTS_DIR / "evaluation_family_holdout.json"
ROBUSTNESS_JSON = RESULTS_DIR / "robustness_results.json"
LATENCY_JSON = RESULTS_DIR / "latency_benchmark.json"
DATASET_SUMMARY_JSON = PROJECT_ROOT / "datasets" / "benchmark_100k" / "dataset_summary.json"
FINAL_RESULTS_CSV = RESULTS_DIR / "FINAL_RESULTS.csv"

# Color Palette (Publication-Grade, Grayscale-Differentiable, Colorblind-Friendly)
COLOR_BENIGN = '#2563eb'     # Royal Blue
COLOR_MALWARE = '#dc2626'    # Crimson Red
COLOR_PROPOSED = '#1d4ed8'   # Deep Blue
COLOR_OPCODE = '#7c3aed'     # Purple
COLOR_CFG = '#059669'        # Emerald Green
COLOR_SYSCALL = '#d97706'    # Amber / Orange
COLOR_FUSION = '#0891b2'     # Cyan / Teal
COLOR_BASELINE = '#64748b'   # Slate Gray
COLOR_GRID = '#e2e8f0'       # Soft Slate
COLOR_TEXT = '#0f172a'       # Deep Navy / Black


def set_springer_style():
    """Applies Springer Nature publication styling to Matplotlib."""
    plt.rcParams.update({
        'font.sans-serif': ['Helvetica', 'Arial', 'DejaVu Sans'],
        'font.family': 'sans-serif',
        'font.size': 10,
        'axes.labelsize': 10.5,
        'axes.titlesize': 11.5,
        'axes.titleweight': 'bold',
        'xtick.labelsize': 9.0,
        'ytick.labelsize': 9.0,
        'legend.fontsize': 9.0,
        'figure.titlesize': 12.0,
        'lines.linewidth': 1.8,
        'axes.linewidth': 0.9,
        'axes.edgecolor': '#94a3b8',
        'grid.linewidth': 0.6,
        'grid.color': COLOR_GRID,
        'grid.linestyle': '--',
        'grid.alpha': 0.7,
        'figure.facecolor': '#ffffff',
        'axes.facecolor': '#ffffff',
        'savefig.facecolor': '#ffffff',
        'savefig.edgecolor': '#ffffff',
        'savefig.bbox': 'tight',
        'savefig.pad_inches': 0.05
    })


def save_figure(fig, base_filename, copy_to_manuscript=None):
    """
    Saves figure in both vector PDF and 300-DPI raster PNG.
    Optionally copies to manuscript figures folder under specified alias.
    """
    pdf_path = OUTPUT_DIR / f"{base_filename}.pdf"
    png_path = OUTPUT_DIR / f"{base_filename}.png"

    fig.savefig(pdf_path, format='pdf')
    fig.savefig(png_path, format='png', dpi=300)
    plt.close(fig)

    print(f"  [SAVED] {pdf_path.name} & {png_path.name}")

    if copy_to_manuscript:
        import shutil
        m_png = MANUSCRIPT_FIG_DIR / f"{copy_to_manuscript}.png"
        shutil.copyfile(png_path, m_png)
        print(f"  [COPIED] -> {m_png.name}")
