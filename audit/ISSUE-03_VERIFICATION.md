# ISSUE-03 Verification Report: Systematic Review Eligibility Audit

**Issue ID:** ISSUE-03  
**Title:** Systematic-review eligibility inconsistency  
**Severity:** Major  
**Status:** **CLOSED — VERIFIED**  
**Date Closed:** October 5, 2026  
**Auditor:** Senior Q1 Journal Systematic Review (PRISMA) Auditor  

---

## 1. Problem Identification
The manuscript reports a PRISMA 2020 systematic review identifying 15 included primary peer-reviewed journal benchmark studies. However, the exact eligibility mapping across the 4 stated Inclusion Criteria:
- **(IC1)** Peer-reviewed journal articles published in indexed venues;
- **(IC2)** Multimodal analysis combining at least two distinct feature modalities;
- **(IC3)** Target domain focused on compiled software binaries (x86, x64, ARM, MIPS);
- **(IC4)** Quantitative reporting of detection or retrieval metrics (Accuracy, F1, AUC, Recall)

had not been compiled into an authoritative study-by-study matrix, raising reviewer concern over potential classification inconsistencies.

---

## 2. Evidence Inspected

1. **Authoritative Bibliographic Records:**
   - 15 study DOIs verified via Crossref metadata.
   - Master evidence matrix compiled in [`audit/systematic_review_eligibility.csv`](file:///Volumes/New%20Storage/Artificial%20Intellgence%20Review/audit/systematic_review_eligibility.csv).
2. **Manuscript Source Files:**
   - [`revised_manuscript/sn-article.tex`](file:///Volumes/New%20Storage/Artificial%20Intellgence%20Review/revised_manuscript/sn-article.tex): Section 6.2 (Eligibility and Screening Criteria, lines 84-89) and Table 1 (Comprehensive evidence matrix, lines 105-131).

---

## 3. Study-by-Study Eligibility Audit Results

| Study ID | Citation & Venue | Article Type | Modalities | IC1 | IC2 | IC3 | IC4 | Eligibility Decision |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **S01** | Gibert et al. (2020), *JNCA* | Review / Survey | Opcode, Byte sequence | YES | YES | YES | YES | **FLAG (Review Article)** |
| **S02** | Landman & Nissim (2021), *Neural Networks* | Primary Research | Dynamic Syscall, Memory Hooks | YES | YES | YES | YES | **KEEP** |
| **S03** | Jiang et al. (2024), *IEEE TSE* | Primary Research | Assembly Tokens, CFG Topology | YES | YES | YES | YES | **KEEP** |
| **S04** | Kim et al. (2023), *IEEE TSE* | Primary Empirical Study | Disassembly Tokens, CFG Topology | YES | YES | YES | YES | **KEEP** |
| **S05** | Han et al. (2026), *ESWA* | Primary Research | CFG Topology, Semantic Opcode Nodes | YES | YES | YES | YES | **KEEP** |
| **S06** | Liu et al. (2023), *IEEE TDSC* | Primary Research | Dynamic API Call Graph, Relational Attributes | YES | YES | YES | YES | **KEEP** |
| **S07** | Qiang et al. (2022), *Computers & Security* | Primary Research | Control Flow Traces, Instruction Semantics | YES | YES | YES | YES | **KEEP** |
| **S08** | Joyce et al. (2023), *Computers & Security* | Primary Reference Dataset | PE Headers, Byte Entropy Metadata | YES | YES | YES | YES | **KEEP** |
| **S09** | Jiang et al. (2024), *Computers & Security* | Primary Benchmark Study | Static PE/Opcode, Dynamic Traces | YES | YES | YES | YES | **KEEP** |
| **S10** | Guerra & Bahsi (2022), *Computers & Security* | Primary Research | Static API Sequences, Opcode/Permissions | YES | YES | YES | YES | **KEEP** |
| **S11** | Alzaylaee et al. (2020), *Computers & Security* | Primary Research | Static Bytecode, Dynamic Device Traces | YES | YES | YES | YES | **KEEP** |
| **S12** | Zhang et al. (2019), *Computers & Security* | Primary Research | Multi-view Static, Dynamic Logs | YES | YES | YES | YES | **KEEP** |
| **S13** | Liu et al. (2023), *Electronics* | Primary Research | Assembly Tokens, CFG Topology | YES | YES | YES | YES | **KEEP** |
| **S14** | Han et al. (2019), *JNCA* | Primary Research | System Call Frequencies & Arguments | YES | FLAG | YES | YES | **FLAG (Modality Granularity)** |
| **S15** | Redhu et al. (2024), *Frontiers in Physics* | Review / Survey | Byte Streams, Opcode Sequences | YES | YES | YES | YES | **FLAG (Review Article)** |

---

## 4. Key Findings & Progression to Issues 04 & 05
- **12 of 15 studies** are verified as unambiguous, primary empirical peer-reviewed journal benchmarks satisfying all four inclusion criteria (IC1–IC4).
- **2 studies (S01, S15)** are survey/review articles that compile existing literature benchmarks rather than novel standalone architectures. They are queued for formal reclassification under **ISSUE-04**.
- **1 study (S14)** uses fine-grained system call argument views, queued for modality boundary adjudication under **ISSUE-05**.
- In accordance with the prompt instructions ("DO NOT immediately delete studies. First reconstruct the eligibility matrix."), the matrix has been formalized in `audit/systematic_review_eligibility.csv` without modifying or fabricating data.

---

## 5. Status Sign-off
**ISSUE-03: CLOSED — VERIFIED**
