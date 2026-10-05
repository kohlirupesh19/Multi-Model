# ISSUE-02 Verification Report: Component Ablation Count Audit

**Issue ID:** ISSUE-02  
**Title:** Ten architectural ablations vs five actually displayed ablations  
**Severity:** Critical  
**Status:** **CLOSED — VERIFIED**  
**Date Closed:** October 5, 2026  
**Auditor:** Senior Q1 Journal Reproducibility & Statistical Auditor  

---

## 1. Problem Identification
In previous manuscript drafts (§1.3 Contributions, item 4), the text claimed:
> *"Ten controlled architectural ablations isolating the marginal contribution of each modality, alignment objective, and fusion mechanism..."*
However, Table 6 only presented five distinct component removal experiments alongside the proposed full framework baseline. Claiming "ten" ablations while displaying only five was an unsubstantiated count inflation.

---

## 2. Evidence Inspected

1. **Repository Configuration & Execution Artifacts:**
   - [`results/ablation_results.json`](file:///Volumes/New%20Storage/Multi-Model/results/ablation_results.json): Contains exactly 6 configuration blocks:
     * `full_model`: Full tri-modal framework (Reference, Acc = 0.9973, F1 = 0.9973)
     * `without_gram`: Ablation 1 (Acc = 0.9680, F1 = 0.9677, $\Delta\text{F1} = -0.0296$)
     * `without_infonce`: Ablation 2 (Acc = 0.9600, F1 = 0.9595, $\Delta\text{F1} = -0.0378$)
     * `without_opcode`: Ablation 3 (Acc = 0.9240, F1 = 0.9229, $\Delta\text{F1} = -0.0744$)
     * `without_cfg`: Ablation 4 (Acc = 0.9407, F1 = 0.9398, $\Delta\text{F1} = -0.0575$)
     * `without_syscall`: Ablation 5 (Acc = 0.9520, F1 = 0.9513, $\Delta\text{F1} = -0.0460$)
   - [`results/verified/component_ablation.csv`](file:///Volumes/New%20Storage/Multi-Model/results/verified/component_ablation.csv): Exactly 6 rows matching `ablation_results.json`.
   - [`tables/verified/table05_component_ablation.csv`](file:///Volumes/New%20Storage/Multi-Model/tables/verified/table05_component_ablation.csv): Matches the 6-row structure.
   - [`tests/test_ablation_consistency.py`](file:///Volumes/New%20Storage/Multi-Model/tests/test_ablation_consistency.py): Tests the marginal degradation of GRAM and InfoNCE.
2. **Manuscript Source Files:**
   - Master LaTeX: [`revised_manuscript/sn-article.tex`](file:///Volumes/New%20Storage/Artificial%20Intellgence%20Review/revised_manuscript/sn-article.tex) (lines 69, 341-361)
   - Master Table 6 (`tab:ablation_results`): Exactly 6 rows (Proposed Full Framework + 5 component removals).

---

## 3. Discrepancy & Verification
- **Count Determination:** The repository contains **exactly five controlled component removal ablations**. There are no 10 ablations in the codebase.
- **Delta-F1 Range Reconciliation:** The earlier text quoted $\Delta\text{F1} = -0.1989$ by mixing the unimodal Syscall baseline from Table 4 ($0.7984 - 0.9973 = -0.1989$) into the ablation claim. Within the actual 5 component ablations (Table 6), the drop ranges from $\Delta\text{F1} = -0.0296$ (GRAM removal) to $\Delta\text{F1} = -0.0744$ (Opcode Transformer branch removal).

---

## 4. Minimum Correction Applied
1. Updated §1.3 Contributions, item 4 ([`sn-article.tex:L69`](file:///Volumes/New%20Storage/Artificial%20Intellgence%20Review/revised_manuscript/sn-article.tex#L69)):
   * Changed: *"Ten controlled architectural ablations isolating the marginal contribution of each modality, alignment objective, and fusion mechanism ($\Delta\text{F1}$ ranging from $-0.0296$ for GRAM removal to $-0.1989$ for unimodal syscall baseline)..."*
   * To: *"Five controlled component ablations isolating the marginal contribution of each modality and alignment objective ($\Delta\text{F1}$ ranging from $-0.0296$ for GRAM removal to $-0.0744$ for Opcode Transformer removal)..."*
2. Ran a global check across the entire manuscript to confirm zero occurrences of "ten ablations" or "10 ablations" remain.
3. Synchronized PDF, DOCX, and repository branches.

---

## 5. Verification Commands and Results

| Check | Command | Expected Output | Actual Output | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Grep Search** | `grep -inE "(ten\|10\|architectural).*ablation" revised_manuscript/sn-article.tex` | 0 inaccurate counts | Only line 59 (literature gap) | **PASS** |
| **Ablation Test** | `python3 -m pytest -v tests/test_ablation_consistency.py` | 1 passed | 1 passed (0.01s) | **PASS** |
| **Full Regression Suite** | `python3 -m pytest -v` | 52 passed | 52 passed (4.44s) | **PASS** |
| **LaTeX Compilation** | `tectonic sn-article.tex` | Exit code 0, 2.72 MB PDF | Exit code 0, 2.72 MB PDF | **PASS** |

---

## 6. Comparison: Before vs. After

### Before:
- Contribution list: *"Ten controlled architectural ablations... ($\Delta\text{F1}$ ranging from $-0.0296$... to $-0.1989$...)"*
- Disconnect: Table 6 only showed 5 component ablations, and $-0.1989$ belonged to Table 4 baseline, not Table 6 ablations.

### After:
- Contribution list: *"Five controlled component ablations isolating the marginal contribution of each modality and alignment objective ($\Delta\text{F1}$ ranging from $-0.0296$ for GRAM removal to $-0.0744$ for Opcode Transformer removal)..."*
- Complete mathematical harmony between Contribution text, §14 Ablation narrative, Table 6, and `results/ablation_results.json`.

---

## 7. Status Sign-off
**ISSUE-02: CLOSED — VERIFIED**
