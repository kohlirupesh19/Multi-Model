# ISSUE-04 Verification Report: Primary Research vs. Review Article Classification Audit

**Issue ID:** ISSUE-04  
**Title:** Primary-study vs review-article classification  
**Severity:** Major  
**Status:** **CLOSED — VERIFIED**  
**Date Closed:** October 5, 2026  
**Auditor:** Senior Q1 Journal Reproducibility & Systematic Review Specialist  

---

## 1. Problem Identification
In previous manuscript iterations, Table 1 was titled *"Comprehensive evidence matrix of the 15 included primary peer-reviewed journal benchmark studies..."*, grouping all 15 included studies as homogeneous primary empirical experiments. 

However, official bibliographic and publisher records reveal that:
1. **S01 (Gibert et al., 2020, JNCA):** *"The rise of machine learning for detection and classification of malware: Research developments, trends and challenges"* is an extensive survey and comparative review.
2. **S15 (Redhu et al., 2024, Front. Phys.):** *"Deep Learning for Malware Detection: A Contemporary Review and Benchmark"* is a systematic literature review synthesizing cross-dataset benchmark performance.

Classifying review and survey papers as purely primary experimental studies without explicit methodological distinction conflates empirical measurement with secondary evidence synthesis.

---

## 2. Evidence Inspected

Authoritative Crossref, publisher metadata, and full-text declarations were audited for all 15 included studies:

| Study ID | First Author | Year | Journal | Publisher DOI | Authoritative Article Type |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **S01** | Gibert et al. | 2020 | JNCA | `10.1016/j.jnca.2019.102464` | **Survey / Comparative Review** |
| **S02** | Landman & Nissim | 2021 | Neural Networks | `10.1016/j.neunet.2021.05.025` | **Primary Empirical Research** |
| **S03** | Jiang et al. | 2024 | IEEE TSE | `10.1109/TSE.2024.3377755` | **Primary Empirical Research** |
| **S04** | Kim et al. | 2023 | IEEE TSE | `10.1109/TSE.2022.3187689` | **Primary Empirical Research** |
| **S05** | Han et al. | 2026 | ESWA | `10.1016/j.eswa.2026.131108` | **Primary Empirical Research** |
| **S06** | Liu et al. | 2023 | IEEE TDSC | `10.1109/TDSC.2022.3216902` | **Primary Empirical Research** |
| **S07** | Qiang et al. | 2022 | Comp & Sec | `10.1016/j.cose.2022.102871` | **Primary Empirical Research** |
| **S08** | Joyce et al. | 2023 | Comp & Sec | `10.1016/j.cose.2022.102921` | **Primary Benchmark Dataset Study** |
| **S09** | Jiang et al. | 2024 | Comp & Sec | `10.1016/j.cose.2024.103706` | **Primary Benchmark Dataset Study** |
| **S10** | Guerra & Bahsi | 2022 | Comp & Sec | `10.1016/j.cose.2022.102835` | **Primary Empirical Research** |
| **S11** | Alzaylaee et al. | 2020 | Comp & Sec | `10.1016/j.cose.2019.101663` | **Primary Empirical Research** |
| **S12** | Zhang et al. | 2019 | Comp & Sec | `10.1016/j.cose.2018.10.001` | **Primary Empirical Research** |
| **S13** | Liu et al. | 2023 | Electronics | `10.3390/electronics12071722` | **Primary Empirical Research** |
| **S14** | Han et al. | 2019 | JNCA | `10.1016/j.jnca.2019.05.011` | **Primary Empirical Research** |
| **S15** | Redhu et al. | 2024 | Front Phys | `10.3389/fphy.2024.1378121` | **Review / Survey Benchmark** |

---

## 3. Discrepancy & Methodological Resolution
- **PRISMA Inclusion vs. Evidence Partitioning:** S01 and S15 meet the criteria of published journal benchmark syntheses (IC1, IC3, IC4) and provide valuable baseline anchor numbers across Drebin/Malimg and Cyberspace corpora. However, they must not be mislabeled as primary laboratory experiments.
- **Resolution Strategy:**
  1. Updated Table 1 with an explicit **`Article Type`** column categorizing each study:
     - `Primary Research` (10 studies)
     - `Empirical Study` (1 study: S04)
     - `Reference Dataset` / `Benchmark Dataset` (2 studies: S08, S09)
     - `Survey Review` (2 studies: S01, S15)
  2. Qualified the count across the manuscript text:
     *"15 included peer-reviewed journal benchmark studies comprising 13 primary empirical investigations and 2 benchmark synthesis reviews"*
  3. Updated Table 1 caption, Abstract, §1.3 Contributions, §6.3 Selection, and Fig. 1 PRISMA Flow caption accordingly.

---

## 4. Minimum Corrections Applied

1. **LaTeX Master File (`revised_manuscript/sn-article.tex`):**
   - Line 15 (Abstract): *"15 included peer-reviewed journal benchmark studies (13 primary empirical investigations and 2 benchmark synthesis reviews)..."*
   - Line 66 (§1.3 Contributions): *"15 included peer-reviewed journal benchmark studies comprising 13 primary empirical investigations and 2 benchmark synthesis reviews..."*
   - Line 92 (§6.3 Selection): *"Exactly 15 peer-reviewed journal benchmark studies were retained: 13 primary empirical investigations and 2 benchmark synthesis reviews (Fig.~\ref{fig:prisma_flow} and Table~\ref{tab:primary_studies})."*
   - Line 97 (Fig. 1 caption): Updated to specify `(13 primary empirical investigations and 2 benchmark synthesis reviews)`.
   - Lines 103–131 (Table 1 `tab:primary_studies`): Introduced column `Article Type`, explicitly tagging S01 as `Survey Review` and S15 as `Survey Review`.
2. **DOCX Builder Script (`audit/scripts/build_manuscript_docx.py`):**
   - Updated Table 1 headers and row structures to include `Article Type`.
   - Re-compiled Word document: `FINAL_REVISED_MANUSCRIPT.docx`.
3. **Repository Synchronizations:**
   - Synchronized `Multi-Model/manuscript/revised/` with updated LaTeX, PDF, and DOCX files.

---

## 5. Verification Commands and Results

| Check | Command | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Study Classification Audit** | `python3 -c "import pandas as pd; df=pd.read_csv('audit/systematic_review_eligibility.csv'); print(df['Article Type'].value_counts())"` | 13 primary/empirical + 2 reviews | 13 primary/benchmark + 2 review/survey | **PASS** |
| **Table 1 Column Integrity** | `grep -F "Article Type" revised_manuscript/sn-article.tex` | Header present in Table 1 | Line 109: `ID & Study & Venue & Article Type & Modalities...` | **PASS** |
| **LaTeX PDF Build** | `tectonic sn-article.tex` | Clean exit 0, valid PDF | Exit code 0, 2.72 MB PDF generated | **PASS** |
| **DOCX Build** | `python3 audit/scripts/build_manuscript_docx.py` | Clean generation | Generated `FINAL_REVISED_MANUSCRIPT.docx` | **PASS** |
| **Regression Test Suite** | `python3 -m pytest "/Volumes/New Storage/Multi-Model/tests" -v` | 52 passed | 52 passed (5.72s) | **PASS** |

---

## 6. Status Sign-off
**ISSUE-04: CLOSED — VERIFIED**
