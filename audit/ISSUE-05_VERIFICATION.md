# ISSUE-05 Verification Report: Multimodal Inclusion Criteria Audit

**Issue ID:** ISSUE-05  
**Title:** Single-modality studies potentially violating inclusion criteria  
**Severity:** Major  
**Status:** **CLOSED — VERIFIED**  
**Date Closed:** October 5, 2026  
**Auditor:** Senior Q1 Journal Reproducibility & Cybersecurity Scientist  

---

## 1. Problem Identification
In previous manuscript iterations, Table 1 abbreviated the modalities column for several studies—most notably **S14 (Han et al., 2019, MalInsight)**, which was labeled solely as *"System Calls"*, creating the appearance that a single-modality dynamic study was incorrectly included in a multimodal binary similarity review. Furthermore, the operational definition of Inclusion Criterion 2 (IC2) lacked explicit boundary definitions distinguishing genuine cross-modality representation spaces from multi-feature unimodal variants (e.g., multiple n-gram window sizes or multiple token filters within a single linear sequence).

---

## 2. Evidence Inspected

Full-text technical methodologies and feature extraction pipelines were audited across all 15 included benchmark studies:

| Study ID | Reference | Modality 1 Space | Modality 2 Space | Orthogonality Assessment | Meets IC2? |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **S01** | Gibert et al. (2020) | Raw Byte Stream (Grayscale Byte Values) | Disassembled Opcodes (Syntactic Assembly) | Static Lexical Byte vs. Syntactic Disassembly | **YES** |
| **S02** | Landman & Nissim (2021) | Dynamic System Calls (API Sequences) | In-Memory Hook States (Kernel Introspection) | Behavioral Execution vs. Memory Telemetry | **YES** |
| **S03** | Jiang et al. (2024) | Assembly Instructions (Linear Disassembly) | Control Flow Graph (Topological Graph) | Lexical Tokens vs. Graph Topology | **YES** |
| **S04** | Kim et al. (2023) | Disassembly Tokens (Normalized Assembly) | Control Flow Graph (Inter-block Topology) | Lexical Tokens vs. Graph Topology | **YES** |
| **S05** | Han et al. (2026) | Control Flow Graph (Graph Topology) | Opcode Semantics (Instruction Node Vectors) | Graph Structure vs. Semantic Node Vectors | **YES** |
| **S06** | Liu et al. (2023) | Dynamic API Graph (Behavioral Call Graph) | API Parameter Attributes (Semantic Attributes) | Execution Graph Topology vs. Parameter Semantics | **YES** |
| **S07** | Qiang et al. (2022) | Control Flow Execution Traces (Dynamic Trace) | Disassembly Opcodes (Instruction Semantics) | Dynamic Control Trace vs. Static Assembly Tokens | **YES** |
| **S08** | Joyce et al. (2023) | PE Section Headers (Structural Metadata) | Byte Entropy Sequences (Spatial Distribution) | Structural Header Metadata vs. Spatial Entropy | **YES** |
| **S09** | Jiang et al. (2024) | Static PE / Opcode Disassembly | Dynamic Behavioral Traces (Cuckoo Sandbox) | Static Disassembly vs. Dynamic Execution Log | **YES** |
| **S10** | Guerra & Bahsi (2022) | Static API / Opcode Sequences | Android Permission Manifest (Declarative Specs) | Static Code Instructions vs. Declarative Metadata | **YES** |
| **S11** | Alzaylaee et al. (2020) | Static Bytecode & Intent Manifest | Dynamic Real-Device API Traces | Static Artifacts vs. Hardware Execution Telemetry | **YES** |
| **S12** | Zhang et al. (2019) | Multi-view Static PE Signatures | Dynamic Behavioral Traces (Execution Logs) | Static Structural Signatures vs. Dynamic Logs | **YES** |
| **S13** | Liu et al. (2023) | Assembly Tokens (Disassembly Sequence) | Control Flow Graph (Topological Structure) | Lexical Tokens vs. Graph Topology | **YES** |
| **S14** | Han et al. (2019) | Static PE Structure (Headers, Sections, Tables) | Dynamic System Call Traces (Execution Sequences) | Static Structural Metadata vs. Dynamic Behavioral Trace | **YES** |
| **S15** | Redhu et al. (2024) | Raw Byte Stream (Byte Sequences) | Opcode Sequences (Disassembled Assembly) | Byte Level Representation vs. Instruction Semantics | **YES** |

---

## 3. Discrepancy & Verification
1. **S14 (MalInsight) Full-Text Audit:**
   - In *MalInsight: A systematic profiling based malware detection framework* (Han et al., 2019, *Journal of Network and Computer Applications*, 125, pp. 236–250, DOI: `10.1016/j.jnca.2018.10.022`), the authors explicitly integrate three tiers: (1) static basic structure (PE header features, section characteristics, imported symbols), (2) high-level dynamic behavior (registry and network activity), and (3) low-level dynamic behavior (system call sequences).
   - Thus, MalInsight is genuinely multimodal, combining static structural metadata with dynamic behavioral execution traces.
   - The manuscript previously labeled S14 solely as *"System Calls"* in Table 1 due to space constraints, inadvertently causing an apparent violation of IC2.
2. **Operational Definition of IC2:**
   - Multimodal binary analysis requires combining features across distinct, orthogonal representation spaces:
     1. Static linear/lexical tokens (e.g., opcodes, byte sequences)
     2. Static/dynamic topological graphs (e.g., CFGs, call graphs)
     3. Dynamic behavioral traces (e.g., system calls, API traces, hook states)
     4. Structural/declarative metadata (e.g., PE section headers, manifest permissions)
   - Combining multiple feature sets from the same space (e.g., 2-gram and 3-gram opcodes) without cross-space fusion is excluded under EC3.

---

## 4. Minimum Correction Applied

1. **LaTeX Master File (`revised_manuscript/sn-article.tex`):**
   - Clarified **IC2** (§6.2, Line 87):
     * *"Multimodal analysis combining at least two distinct feature modalities across orthogonal representation spaces (static lexical/token sequences, static/dynamic topological graphs, dynamic behavioral traces, and structural/declarative metadata);"*
   - Clarified **EC3** (§6.2, Line 88):
     * *"Work limited strictly to unimodal analysis or single-space feature variations (e.g., combining multiple static n-gram lengths without cross-space multimodal fusion);"*
   - Updated **Table 1 (`tab:primary_studies`) Modalities Column**:
     * S06: `Dynamic Graph, API`
     * S07: `CFG Traces, Opcodes`
     * S08: `PE Headers, Entropy`
     * S09: `Static PE, Dynamic Logs`
     * S10: `API, Manifest Permissions`
     * S11: `Static Bytecode, Dynamic Traces`
     * S12: `Static PE, Dynamic Logs`
     * S14: `Static PE, Syscalls` (Han et al., 2019, MalInsight)
2. **Systematic Review Eligibility Matrix (`audit/systematic_review_eligibility.csv`):**
   - Updated S14 with verified title (*"MalInsight: A systematic profiling based malware detection framework"*), verified author list, verified DOI (`10.1016/j.jnca.2018.10.022`), explicit modalities (*Static PE Structure*, *Dynamic Syscall Traces*), and status `KEEP`.
   - Updated S01 DOI to verified resolution `10.1016/j.jnca.2019.102464`.
3. **Artifact Synchronizations:**
   - Synchronized LaTeX, PDF, DOCX, and CSV artifacts to `/Volumes/New Storage/Multi-Model/`.

---

## 5. Verification Commands and Results

| Check | Command | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **All Studies Satisfy IC2** | `python3 -c "import pandas as pd; df=pd.read_csv('audit/systematic_review_eligibility.csv'); print((df['Meets IC2?'] == 'YES').all())"` | `True` (all 15 studies meet IC2) | `True` | **PASS** |
| **Table 1 Modalities Completeness** | `grep -F "Static PE, Syscalls" revised_manuscript/sn-article.tex` | Modality match in S14 | `S14 & Han et al. ... & Static PE, Syscalls & ...` | **PASS** |
| **LaTeX PDF Build** | `tectonic sn-article.tex` | Exit code 0, 2.72 MB PDF | Exit code 0, 2.72 MB PDF | **PASS** |
| **DOCX Build** | `python3 audit/scripts/build_manuscript_docx.py` | Exit code 0, DOCX updated | Clean generation | **PASS** |
| **Regression Test Suite** | `python3 -m pytest "/Volumes/New Storage/Multi-Model/tests" -v` | 52 passed | 52 passed (4.21s) | **PASS** |

---

## 6. Status Sign-off
**ISSUE-05: CLOSED — VERIFIED**
