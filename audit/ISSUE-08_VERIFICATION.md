# ISSUE-08 Verification Report: Irrelevant References Audit

**Issue ID:** ISSUE-08  
**Title:** Irrelevant references [24]–[26]  
**Severity:** Minor (Thematic & Scientific Integrity)  
**Status:** **CLOSED — VERIFIED**  
**Date Closed:** October 5, 2026  
**Auditor:** Senior Q1 Journal Peer-Review Auditor & Manuscript Editor  

---

## 1. Problem Identification

In §2 (Related Work), previous drafts contained the following standalone claim:
> *"In cyber-physical and power grid infrastructures, machine learning-driven anomaly detection has demonstrated critical defensive utility against false-data injection and network-level intrusion \cite{Almalaq2023Power,Almalaq2022Deep,Alnowibet2021Energy}."*

The three cited works were:
1. **Almalaq et al. (2023):** *"An Adoptive Miner-Misuse Based Online Anomaly Detection Approach in the Power System: An Optimum Reinforcement Learning Method"*, *Mathematics*, DOI: `10.3390/math11040884`.
2. **Almalaq et al. (2022):** *"Deep Machine Learning Model-Based Cyber-Attacks Detection in Smart Power Systems"*, *Mathematics*, DOI: `10.3390/math10152574`.
3. **Alnowibet et al. (2021):** *"Effective Energy Management via False Data Detection Scheme for the Interconnected Smart Energy Hub--Microgrid System under Stochastic Framework"*, *Sustainability*, DOI: `10.3390/su132111836`.

---

## 2. Evidence Inspected & Scope Assessment

1. **Topical Scope of Manuscript:**
   - The paper focuses strictly on **Adaptive Tri-Modal Malware Detection with Contrastive Cross-Modal Representation Learning and Operational Triage** for compiled Windows Portable Executable (PE) binaries.
   - The architectural components comprise Opcode Transformers (static lexical tokens), CFG Graph Isomorphism Networks (topological control flow), and dynamic System Call Bi-LSTMs (runtime behavioral traces).
2. **Evaluation of Manuscript Claims Supported:**
   - A full-text grep audit revealed that smart power systems, microgrids, energy hubs, and false-data injection were never discussed in the Abstract, Introduction, Methodology, Experiments, Results, Discussion, Limitations, or Conclusion.
   - The single sentence in §2 was an isolated citation insertion (historically introduced to satisfy a non-topical reviewer request).
   - Because no meaningful methodological or empirical claim in the paper relies on or investigates power grid microgrid dynamics, retaining these references introduced thematic dissonance and vulnerability to editorial criticism regarding citation gaming.

---

## 3. Discrepancy & Editorial Resolution

- **Resolution Policy:**
  * As dictated by the task instructions: *"If no meaningful claim requires it: remove it."*
  * The isolated sentence in §2 Related Work was removed.
  * The three references (`Almalaq2023Power`, `Almalaq2022Deep`, and `Alnowibet2021Energy`) were purged from `sn-bibliography.bib`.
- **Resulting Paragraph Coherence:**
  * The paragraph in §2 now reads smoothly and logically:
    > *"Multimodal learning seeks to unify these orthogonal perspectives \cite{Baltrusaitis2019}. Recent contrastive frameworks leverage InfoNCE and multi-view objectives to align cross-modal embeddings \cite{LeKhac2020,FewMHGCL2023,BinCola2024}. Concurrently, longitudinal evaluation protocols have underscored the impact of concept drift and dataset shift over time \cite{Joyce2023MOTIF,Jiang2024BenchMFC,Guerra2022}. Nevertheless, prior multimodal works frequently lack open evaluation tensors and fail to delineate operational triage boundaries."*
  * The transition from cross-modal contrastive embeddings and concept drift directly to multimodal triage gaps is now coherent and scientifically sound.

---

## 4. Minimum Correction Applied

1. **LaTeX Source (`revised_manuscript/sn-article.tex`):**
   - Line 77: Removed the extraneous sentence citing Almalaq and Alnowibet.
2. **BibTeX Database (`revised_manuscript/sn-bibliography.bib`):**
   - Deleted the three entries (`Almalaq2023Power`, `Almalaq2022Deep`, `Alnowibet2021Energy`), reducing total active bibliography entries to exactly 26.
3. **Artifact Compilation & Synchronization:**
   - Recompiled `sn-article.pdf` via `tectonic --keep-intermediates`.
   - Rebuilt `FINAL_REVISED_MANUSCRIPT.docx` (updated reference list to 26 items).
   - Synchronized all files across workspace and `/Volumes/New Storage/Multi-Model/`.

---

## 5. Verification Commands and Results

| Check | Command | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Purged Citations in Tex** | `grep -E "Almalaq|Alnowibet" revised_manuscript/sn-article.tex` | 0 matches | 0 matches | **PASS** |
| **Purged Entries in Bib** | `grep -E "Almalaq|Alnowibet" revised_manuscript/sn-bibliography.bib` | 0 matches | 0 matches | **PASS** |
| **Active Reference Count** | `grep -c "%%%" revised_manuscript/sn-article.bbl` | Exactly 26 references | 26 references | **PASS** |
| **LaTeX PDF Build** | `tectonic sn-article.tex` | Exit code 0, clean PDF | Exit code 0, 2.72 MB PDF | **PASS** |
| **DOCX Build** | `python3 audit/scripts/build_manuscript_docx.py` | Exit code 0, clean DOCX | Clean DOCX generation | **PASS** |
| **Regression Test Suite** | `python3 -m pytest "/Volumes/New Storage/Multi-Model/tests" -v` | 52 passed | 52 passed (4.38s) | **PASS** |

---

## 6. Status Sign-off
**ISSUE-08: CLOSED — VERIFIED**
