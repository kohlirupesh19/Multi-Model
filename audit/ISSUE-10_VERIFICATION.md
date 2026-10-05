# Verification Report: ISSUE-10 — Baseline Classification and Reproduction Terminology

## Verification Gate Report

-------------------------------------
ISSUE: ISSUE-10 — Baseline Classification and Reproduction Terminology
-------------------------------------

### Problem:
The baseline section previously exhibited terminology ambiguity by referring generally to all baseline models as "internally reproduced" without distinguishing between:
1. Native repository components evaluated as unimodal or early-fusion baselines,
2. Full neural benchmark architectures reimplemented from published specifications (MalConv), and
3. Unsupervised binary function similarity/retrieval models (Gemini Structure2Vec and Asm2Vec Word2Vec) that cannot perform malware detection out of the box and must be adapted with an explicit classification head.

### Evidence Inspected:
- `Research Paper/FINAL_RESULTS.csv`: Experiments `EXP-16-BASELINE-OPCODE` to `EXP-22-BASELINE-CONCAT` and `EXP-01-PROPOSED-TEST`.
- `tests/test_benchmark_integrity.py`: Baseline metric assertions and evaluation parameters.
- `tests/test_result_reproducibility.py`: Cross-validation of model evaluation metrics.
- `reproduce_all.py`: Table generation logic for baseline comparisons.
- `Research Paper/revised_manuscript/sn-article.tex`: Section 12 (\ref{sec:baselines}) and Section 13 (\ref{tab:benchmark_comparison}).

### Repository Files:
- `reproduce_all.py`
- `Research Paper/revised_manuscript/sn-article.tex`
- `tables/verified/table04_baseline_comparison.csv`

### Manuscript Location:
- Section 12 (`\ref{sec:baselines}`): Detailed baseline inventory and architectural description.
- Section 13 (`\ref{tab:benchmark_comparison}`): Table 3 ("Comparative benchmark evaluation on the held-out test partition ($N = 1,500$)...").

### Current State:
All 8 architectures are rigorously categorized and documented:
1. **Proposed Architecture**: Proposed Tri-Modal (Opcode + CFG + Syscall + GRAM) — Acc 99.73%, F1 0.9973.
2. **Internally Reproduced**:
   - Concat MLP (Early Fusion): Acc 93.80%, F1 0.9370
   - Opcode Transformer Only: Acc 86.47%, F1 0.8627
   - CFG-GIN Only: Acc 84.20%, F1 0.8400
   - Syscall Bi-LSTM Only: Acc 80.07%, F1 0.7984
3. **Reimplemented Benchmark**:
   - MalConv Gated CNN: Byte-level CNN with temporal global max-pooling, reimplemented based on Gibert et al. (Acc 88.20%, F1 0.8805).
4. **Adapted & Reimplemented**:
   - Gemini Structure2Vec: ACFG message passing ($d=128$) adapted with 2-layer MLP head trained via cross-entropy (Acc 85.40%, F1 0.8521).
   - Asm2Vec Word2Vec: PV-DM assembly token random walk embeddings ($d=128$) adapted with 2-layer MLP head trained via cross-entropy (Acc 87.13%, F1 0.8697).

The adaptation pipelines are fully documented in Section 12:
- Representation: 128-dimensional latent vector
- Classifier: Supervised 2-layer MLP classification head
- Training data: Identical 7,000 training partition samples
- Test data: Identical 1,500 test partition samples
- Decision threshold: $\theta = 0.50$

### Correction Made:
1. Updated `reproduce_all.py` `classify_baseline()` function to programmatically assign the precise categories (`Proposed Architecture`, `Internally Reproduced`, `Reimplemented Benchmark`, `Adapted & Reimplemented`) in `tables/verified/table04_baseline_comparison.csv`.
2. Verified that Section 12 and Table 3 (`tab:benchmark_comparison`) in `Research Paper/revised_manuscript/sn-article.tex` explicitly report this classification taxonomy.
3. Compiled PDF (`sn-article.pdf`) and rebuilt DOCX (`FINAL_REVISED_MANUSCRIPT.docx`).

### Tests Executed:
- Full test suite: `python3 -m pytest tests/ -v` (52 tests passed).
- End-to-end reproducibility pipeline: `python3 reproduce_all.py`.
- Manuscript compilation: `tectonic --keep-intermediates sn-article.tex`.

### Test Command:
```bash
python3 -m pytest "/Volumes/New Storage/Multi-Model/tests" -v
python3 "/Volumes/New Storage/Artificial Intellgence Review/reproduce_all.py"
```

### Expected:
- All 52 automated tests pass.
- `tables/verified/table04_baseline_comparison.csv` contains column `Category` with exact classification mappings.
- No unsubstantiated literature claims or vague "internally reproduced" misnomers remain.

### Actual:
- 52/52 tests passed in 4.43 seconds.
- Table 4 CSV matches Table 3 LaTeX and DOCX exactly.
- LaTeX compilation completed with 0 errors.

### PASS/FAIL:
PASS

### Regression Check:
- Primary test metrics: TP=740, TN=756, FP=0, FN=4, Acc=99.73%, F1=0.9973.
- Split disjointness: 0 overlap between Train (7,000), Val (1,500), and Test (1,500).
- Robustness (UPX, Dead Code, CFG Flattening, Sandbox Stalling): identical to verified logs.

### Evidence Generated:
- `tables/verified/table04_baseline_comparison.csv`
- `audit/ISSUE-10_VERIFICATION.md`
- `FINAL_REVISED_MANUSCRIPT.pdf`
- `FINAL_REVISED_MANUSCRIPT.docx`

### Commit/Hash:
Pending git commit for ISSUE-10 closure.

### Status:
CLOSED — VERIFIED
