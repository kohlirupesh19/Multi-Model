# ISSUE-01 Verification Report: Robustness Transformations Count

**Issue ID:** ISSUE-01  
**Title:** Five adversarial obfuscations vs four reported transformations  
**Severity:** Critical  
**Status:** **CLOSED — VERIFIED**  
**Date Closed:** October 5, 2026  
**Auditor:** Senior Q1 Journal Reproducibility & Statistical Auditor  

---

## 1. Problem Identification
Earlier manuscript drafts referenced "five adversarial obfuscations", but the empirical tables (Table 6/7) only presented four distinct adversarial transformations (UPX packing, dead-code insertion, CFG flattening, and sandbox stalling) alongside an unperturbed clean baseline. This created an internal contradiction between the introductory/abstract text and the actual experimental results.

---

## 2. Evidence Inspected

1. **Repository Configuration & Execution Data:**
   - [`results/robustness_results.json`](file:///Volumes/New%20Storage/Multi-Model/results/robustness_results.json): Contains exactly 5 condition blocks:
     * `clean` (Nominal unperturbed baseline)
     * `upx_packing` (Adversarial transformation 1)
     * `dead_code_insertion` (Adversarial transformation 2)
     * `cfg_flattening` (Adversarial transformation 3)
     * `sandbox_stalling` (Adversarial transformation 4)
   - [`results/verified/robustness.csv`](file:///Volumes/New%20Storage/Multi-Model/results/verified/robustness.csv): Contains exactly 1 clean baseline row and 4 transformation rows.
   - [`tables/verified/table07_robustness.csv`](file:///Volumes/New%20Storage/Multi-Model/tables/verified/table07_robustness.csv): Matches the 5-row structure.
   - [`multimodal_malware/training/dataset.py:L63`](file:///Volumes/New%20Storage/Multi-Model/multimodal_malware/training/dataset.py#L63) and [`multimodal_malware/app.py:L213`](file:///Volumes/New%20Storage/Multi-Model/multimodal_malware/app.py#L213): Implements and documents the 4 perturbations.
2. **Manuscript Source Files:**
   - Master LaTeX: [`revised_manuscript/sn-article.tex`](file:///Volumes/New%20Storage/Artificial%20Intellgence%20Review/revised_manuscript/sn-article.tex)
   - Compiled PDF: [`FINAL_REVISED_MANUSCRIPT.pdf`](file:///Volumes/New%20Storage/Artificial%20Intellgence%20Review/FINAL_REVISED_MANUSCRIPT.pdf)
   - Word Document: [`FINAL_REVISED_MANUSCRIPT.docx`](file:///Volumes/New%20Storage/Artificial%20Intellgence%20Review/FINAL_REVISED_MANUSCRIPT.docx)

---

## 3. Current State & Discrepancies Resolved
- **Count Determination:** The experimental design contains **exactly four independently executed adversarial code transformations** and **one unperturbed clean baseline**. There is no fifth transformation in the codebase or experiment artifacts.
- **Attention Weights Realignment in Table 7:** During raw data inspection of `results/robustness_results.json`, it was discovered that under `sandbox_stalling`, the dynamic trace is dropped, forcing $\alpha_{\text{sys}} = 0.000, \alpha_{\text{op}} = 0.790, \alpha_{\text{cfg}} = 0.210$. The manuscript table had previously listed intermediate weights ($0.627, 0.175, 0.198$). Table 7 has been updated to reflect the exact raw values: $\alpha_{\text{op}} = 0.790, \alpha_{\text{cfg}} = 0.210, \alpha_{\text{sys}} = 0.000$.

---

## 4. Minimum Correction Applied
1. Verified that zero occurrences of "five adversarial" or "five obfuscation" or "five transformations" remain in the manuscript.
2. Verified all references in text, contributions, robustness section, Table 7 caption, and Fig. 8 caption read:
   *"four adversarial code transformations (UPX packing, dead-code insertion, control-flow flattening, and sandbox stalling) evaluated alongside an unperturbed clean baseline."*
3. Updated Table 7 row 5 to match the raw output attention values ($0.790, 0.210, 0.000$).

---

## 5. Verification Commands and Results

| Check | Command | Expected Output | Actual Output | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Grep Search** | `grep -inE "five.*(adversarial\|obfuscation\|transformation\|perturbation)" revised_manuscript/sn-article.tex` | 0 matches | 0 matches | **PASS** |
| **Robustness Test** | `python3 -m pytest -v tests/test_benchmark_integrity.py::test_upx_robustness_metrics` | 1 passed | 1 passed (0.74s) | **PASS** |
| **Full Regression Suite** | `python3 -m pytest -v` | 52 passed | 52 passed (6.16s) | **PASS** |
| **LaTeX Compilation** | `tectonic sn-article.tex` | Exit code 0, 2.72 MB PDF | Exit code 0, 2.72 MB PDF | **PASS** |

---

## 6. Comparison: Before vs. After

### Before:
- Manuscript text: Inconsistent wording claiming "five adversarial obfuscations" while listing 4 transformations.
- Table 7: Listed Sandbox Stalling attention as $0.627, 0.175, 0.198$ (diverging from raw output).

### After:
- Manuscript text: Unambiguously states *"four adversarial code transformations (UPX packing, dead-code insertion, control-flow flattening, and sandbox stalling) evaluated alongside an unperturbed clean baseline."*
- Table 7: Exactly matches raw repository output `results/robustness_results.json`:
  * Clean Baseline: Acc = 100.00%, F1 = 1.0000, Prec = 100.00%, Rec = 100.00%, FPR = 0.00%, FNR = 0.00%, $\alpha = [0.606, 0.173, 0.221]$
  * UPX Packing: Acc = 88.00%, F1 = 0.8929, Prec = 80.65%, Rec = 100.00%, FPR = 24.00%, FNR = 0.00%, $\alpha = [0.389, 0.267, 0.343]$
  * Dead-Code Insertion: Acc = 80.00%, F1 = 0.7500, Prec = 100.00%, Rec = 60.00%, FPR = 0.00%, FNR = 40.00%, $\alpha = [0.528, 0.206, 0.267]$
  * CFG Flattening: Acc = 96.00%, F1 = 0.9583, Prec = 100.00%, Rec = 92.00%, FPR = 0.00%, FNR = 8.00%, $\alpha = [0.616, 0.166, 0.219]$
  * Sandbox Stalling: Acc = 98.00%, F1 = 0.9796, Prec = 100.00%, Rec = 96.00%, FPR = 0.00%, FNR = 4.00%, $\alpha = [0.790, 0.210, 0.000]$

---

## 7. Status Sign-off
**ISSUE-01: CLOSED — VERIFIED**
