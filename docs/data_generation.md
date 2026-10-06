# Synthetic Multimodal Benchmark Generation Specification & Audit (Phase 5)

## 1. Algorithmic Pseudocode

```text
Algorithm: GenerateSingleSample(i, TotalSamples, Balanced)
Input: Sample index i, total catalog size N, class balance flag
Output: Multi-modal sample dictionary S_i

1. rng <- Random(Seed = 42 + i)
2. If Balanced is True:
       If i % 2 == 0:
           Label y_i <- 0 (Benign)
           ProfileIndex <- (i // 2) mod |BenignProfiles|
           Profile P_i <- BenignProfiles[ProfileIndex]
       Else:
           Label y_i <- 1 (Malware)
           ProfileIndex <- (i // 2) mod |MalwareProfiles|
           Profile P_i <- MalwareProfiles[ProfileIndex]
3. FileSize <- rng.UniformInt(15000, 500000)
4. Entropy <- Round(rng.Uniform(P_i.EntropyMin, P_i.EntropyMax), 3)
5. Timestamp <- 1680000000 + (i mod 365) * 86400
6. Sample Opcode sequence O_i from P_i.Ops with P_i.Weights; abstract operands to <REG>, <MEM>, <IMM>
7. Construct BasicBlocks B_1..B_k where k ~ Uniform(P_i.MinBlocks, P_i.MaxBlocks)
   With conditional branch transfers governed by P_i.BranchProb
8. Build CFG Graph G_i = (V, E, X) where X in R^{|V| x 16}
9. Dynamic availability m_s <- (rng.Uniform(0, 1) > 0.12)
   If m_s == 1:
       Sample API trace S_i from P_i.APIs + CommonAPIs
   Else:
       Trace S_i <- Empty, m_s <- 0
10. Return S_i = {sha256, label, family, entropy, timestamp, opcode_tensor, cfg_data, syscall_tensor, has_syscall}
```

## 2. Determinism Verification

Deterministic random state binding (`rng = random.Random(42 + i)`) guarantees strict reproducibility:
- For identical index $i$, `generate_single_sample(i)` produces bitwise identical tensors, graph topologies, and metadata.
- For distinct indices $i \neq j$, samples represent statistically distinct instances parameterized by their respective behavioral profiles.

## 3. Disjoint Partitioning Protocols

1. **Nominal Stratified Split (Within-Profile Benchmark):**
   - Active corpus: Indices $0 \dots 9,999$ ($N=10,000$).
   - 7,000 training (70%), 1,500 validation (15%), 1,500 held-out test (15%).
   - All 10 profiles present in train and test.
2. **Generator-Seed-Disjoint Generalization Split:**
   - Evaluated on indices $50,000 \dots 51,499$ ($N=1,500$).
   - Generator seeds: $50,042 \dots 51,541$ (Seed overlap = 0).
   - Timestamp epoch shifted by 365 days (Calendar day overlap = 0).
   - Sample contamination = 0.
