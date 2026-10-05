# Master Issue Register (Audited Q1 Remediation Protocol)

**Project:** Adaptive Tri-Modal Malware Detection with Contrastive Cross-Modal Representation Learning and Operational Triage  
**Repository:** `https://github.com/kohlirupesh19/Multi-Model.git`  
**Working Remediation Branch:** `publication-remediation`  
**Baseline Commit Hash:** `762c4c858301d578d1ac81ce265b80e6a2941ec8`  
**Date Initialized:** October 5, 2026  

---

## Issue Status Ledger

| Issue ID | Description / Area | Severity | Priority Order | Current Status | Verification Artifact |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ISSUE-01** | Five adversarial obfuscations vs four reported transformations | Critical | 1 | **CLOSED — VERIFIED** | `audit/ISSUE-01_VERIFICATION.md` |
| **ISSUE-02** | Ten architectural ablations vs five actually displayed ablations | Critical | 2 | **CLOSED — VERIFIED** | `audit/ISSUE-02_VERIFICATION.md` |
| **ISSUE-03** | Systematic-review eligibility inconsistency | Major | 3 | **CLOSED — VERIFIED** | `audit/systematic_review_eligibility.csv` |
| **ISSUE-04** | Primary-study vs review-article classification | Major | 4 | **UNDER AUDIT** | `audit/ISSUE-04_VERIFICATION.md` |
| **ISSUE-05** | Single-modality studies potentially violating inclusion criteria | Major | 5 | QUEUED | `audit/ISSUE-05_VERIFICATION.md` |
| **ISSUE-06** | F1 confidence interval methodology/terminology | Major | 6 | QUEUED | `results/verified/statistical_metrics.json` |
| **ISSUE-07** | Reference [16] bibliographic error | Minor | 7 | QUEUED | `audit/ISSUE-07_VERIFICATION.md` |
| **ISSUE-08** | Irrelevant references [24]–[26] | Minor | 8 | QUEUED | `audit/ISSUE-08_VERIFICATION.md` |
| **ISSUE-09** | "Q1 Journal" incorrectly appearing as the venue of the current study | Minor | 9 | QUEUED | `audit/ISSUE-09_VERIFICATION.md` |
| **ISSUE-10** | Baseline classification/reproduction terminology | Major | 10 | QUEUED | `audit/ISSUE-10_VERIFICATION.md` |
| **ISSUE-11** | Temporal evaluation terminology | Critical | 11 | QUEUED | `audit/ISSUE-11_VERIFICATION.md` |
| **ISSUE-12** | WannaCry/family-holdout claim scope | Major | 12 | QUEUED | `audit/ISSUE-12_VERIFICATION.md` |
| **ISSUE-13** | Production-deployment claim strength | Major | 13 | QUEUED | `audit/ISSUE-13_VERIFICATION.md` |
| **ISSUE-14** | Latency terminology and end-to-end scope | Critical | 14 | QUEUED | `audit/ISSUE-14_VERIFICATION.md` |
| **ISSUE-15** | Data availability wording | Major | 15 | QUEUED | `audit/ISSUE-15_VERIFICATION.md` |
| **ISSUE-16** | Mathematical/notation consistency | Major | 16 | QUEUED | `audit/equation_implementation_matrix.csv` |
| **ISSUE-17** | Cross-section numerical consistency | Critical | 17 | QUEUED | `audit/numerical_dictionary.csv` |
| **ISSUE-18** | Statistical methodology audit | Major | 18 | QUEUED | `audit/statistical_audit_report.md` |
| **ISSUE-19** | Reference/DOI/indexing verification | Major | 19 | QUEUED | `audit/reference_verification.csv` |
| **ISSUE-20** | Final clean-clone reproducibility verification | Critical | 20 | QUEUED | `audit/reproducibility_report.md` |

---

## Execution Protocol Constraint
- Under the strict sequential policy, **ONLY ONE ISSUE IS PROCESSED AT A TIME**.
- The next issue will NOT be touched until the current issue passes targeted and regression verification, is documented in its dedicated verification report, and is frozen.
