# Split and Preprocessing Leakage Audit

- Train ∩ Val: 0 hashes
- Train ∩ Test: 0 hashes
- Val ∩ Test: 0 hashes
- **Preprocessing Leakage:** Feature extractors, opcode tokenizers, and normalization dictionaries use fixed global vocabularies fitted strictly prior to inference without test leakage.
