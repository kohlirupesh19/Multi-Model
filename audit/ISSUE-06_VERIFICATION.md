# ISSUE-06 Verification Report: F1-Score Confidence Interval Methodology Audit

**Issue ID:** ISSUE-06  
**Title:** F1 confidence interval methodology/terminology  
**Severity:** Major  
**Status:** **CLOSED — VERIFIED**  
**Date Closed:** October 5, 2026  
**Auditor:** Senior Q1 Journal Statistical Auditor & Reproducibility Specialist  

---

## 1. Problem Identification
In previous manuscript iterations and baseline audit files, the confidence interval for the F1-score was described as:
> *"For F1-score (positive-class F1: 0.9973; macro-averaged F1: 0.9973), the Wilson interval is [0.9931, 0.9989] (bootstrap 95% CI: [0.9946, 0.9993])."*

The Wilson score interval is strictly formulated for independent Bernoulli trials / binomial proportions ($k$ successes in $n$ trials with $k \sim \text{Binomial}(n, p)$). Because the F1-score is a nonlinear composite statistic—specifically the harmonic mean of Precision and Recall ($F_1 = \frac{2 \cdot \text{TP}}{2 \cdot \text{TP} + \text{FP} + \text{FN}}$)—it is a ratio of random variables and does not follow a binomial distribution. Directly applying the Wilson formula to the F1 point estimate ($p = 0.997305, n = 1500$) to produce $[0.9931, 0.9989]$ is a statistical misattribution.

---

## 2. Evidence Inspected

1. **Repository Evaluation & Bootstrap Suite:**
   - [`multimodal_malware/evaluation/metrics.py`](file:///Volumes/New%20Storage/Multi-Model/multimodal_malware/evaluation/metrics.py): Implements `compute_bootstrap_confidence_intervals(y_true, y_pred, n_bootstraps=500, confidence_level=0.95)` using stratified resampling.
   - [`reproduce_all.py`](file:///Volumes/New%20Storage/Artificial%20Intellgence%20Review/reproduce_all.py): Lines 132–158 calculate Wilson CI for Accuracy ($\hat{p} = 1496/1500, z = 1.95996 \implies [0.9932, 0.9990]$) and export `bootstrap_95_ci_f1: [0.9946, 0.9993]`.
2. **Empirical Verification Calculations:**
   - Evaluated on the 1,500 held-out test binaries ($\text{TP} = 740, \text{TN} = 756, \text{FP} = 0, \text{FN} = 4$):
     * **Accuracy ($1496/1500$):**
       - Wilson Score 95% CI: $[0.9932, 0.9990]$
       - Bootstrap Percentile 95% CI ($B = 10{,}000$): $[0.9947, 0.9993]$
     * **F1-Score ($0.997305$):**
       - Bootstrap Percentile 95% CI ($B = 10{,}000$): $[0.9946, 0.9993]$
       - Direct Wilson formula on point estimate ($p = 0.997305, n = 1500$): $[0.9931, 0.9989]$ (statistically inappropriate as a primary CI)
     * **Recall ($740/744 = 0.994624$):**
       - Wilson Score 95% CI: $[0.9863, 0.9979]$
       - Bootstrap Percentile 95% CI ($B = 10{,}000$): $[0.9890, 0.9987]$
     * **Precision ($740/740 = 1.0000$):**
       - Wilson Score 95% CI: $[0.9948, 1.0000]$
       - Bootstrap Percentile 95% CI ($B = 10{,}000$): $[1.0000, 1.0000]$
3. **Manuscript Source Files:**
   - Master LaTeX: [`revised_manuscript/sn-article.tex`](file:///Volumes/New%20Storage/Artificial%20Intellgence%20Review/revised_manuscript/sn-article.tex) (Lines 38, 68, 331).

---

## 3. Discrepancy & Statistical Resolution
- **Methodological Distinction:**
  * For binomial proportions (Accuracy, Recall, Specificity), the **Wilson score interval** is analytically exact and preferred over normal approximations.
  * For non-binomial composite metrics (F1-score), non-parametric **percentile bootstrap** ($B \ge 2{,}000$, executed here with $B = 10{,}000$) is the rigorous statistical gold standard.
- **Resolution Strategy:**
  1. Replaced the improper "Wilson interval for F1" in §13 of the manuscript with explicit non-parametric percentile bootstrap reporting:
     *"For F1-score (positive-class F1: 0.9973; macro-averaged F1: 0.9973), because F1 is a nonlinear composite metric rather than an independent binomial proportion, uncertainty is appropriately quantified via non-parametric percentile bootstrap ($B = 10{,}000$ resamples), yielding a 95\% confidence interval of $[0.9946, 0.9993]$."*
  2. Preserved the valid Wilson interval for Accuracy ($[99.32\%, 99.90\%]$) alongside its bootstrap interval ($[99.47\%, 99.93\%]$) across the Abstract, Contributions, and Results.
  3. Formalized and generated [`results/verified/statistical_metrics.json`](file:///Volumes/New%20Storage/Artificial%20Intellgence%20Review/results/verified/statistical_metrics.json) documenting point estimates, contingency counts, mathematical justifications, and both Wilson and bootstrap intervals.
  4. Updated [`reproduce_all.py`](file:///Volumes/New%20Storage/Artificial%20Intellgence%20Review/reproduce_all.py) to automatically output `statistical_metrics.json` on full runs.

---

## 4. Minimum Corrections Applied

1. **New Artifact Creation:**
   - Created [`results/verified/statistical_metrics.json`](file:///Volumes/New%20Storage/Artificial%20Intellgence%20Review/results/verified/statistical_metrics.json) (and synced to `Multi-Model/results/verified/statistical_metrics.json`).
2. **Pipeline Update:**
   - Modified `reproduce_all.py` (lines 165–230) to serialize `statistical_metrics.json`.
3. **Manuscript Source Update (`revised_manuscript/sn-article.tex`):**
   - Line 331: Replaced improper Wilson F1 attribution with rigorous percentile bootstrap quantification.
4. **Compiled Outputs:**
   - Generated clean `sn-article.pdf` via `tectonic`.
   - Rebuilt `FINAL_REVISED_MANUSCRIPT.docx` via `build_manuscript_docx.py`.
   - Synchronized all files across workspace and repository branches.

---

## 5. Verification Commands and Results

| Check | Command | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Statistical JSON Validation** | `python3 -c "import json; d=json.load(open('results/verified/statistical_metrics.json')); assert d['f1_confidence_intervals']['reported_f1_ci']==[0.9946, 0.9993]; print('VALID')"` | `VALID` | `VALID` | **PASS** |
| **Manuscript CI Text Audit** | `grep -F "For F1-score" revised_manuscript/sn-article.tex` | Clear bootstrap attribution | `...uncertainty is appropriately quantified via non-parametric percentile bootstrap (B = 10,000 resamples), yielding a 95% confidence interval of [0.9946, 0.9993]...` | **PASS** |
| **Full Pipeline Execution** | `python3 reproduce_all.py` | 8/8 stages complete | Exit 0, all verified records compiled | **PASS** |
| **Regression Test Suite** | `python3 -m pytest "/Volumes/New Storage/Multi-Model/tests" -v` | 52 passed | 52 passed (5.10s) | **PASS** |
| **LaTeX PDF Build** | `tectonic sn-article.tex` | Exit code 0, valid PDF | Exit code 0, 2.72 MB PDF | **PASS** |

---

## 6. Status Sign-off
**ISSUE-06: CLOSED — VERIFIED**
