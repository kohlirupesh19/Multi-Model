# System Architecture and Mathematical Formulation

This document details the multi-modal neural architecture, contrastive representation learning objectives, and availability-aware late fusion mechanism implemented in `multimodal_malware/models/`.

---

## 1. Architectural Pipeline

The detection pipeline maps heterogeneous executable binary signals into aligned latent representations:

```
[Executable Binary]
       │
       ├── Disassembly ────> Opcode Sequence (2048) ────> Opcode Transformer ───> z_opcode  (128d)
       │                                                                               │
       ├── Graph Parsing ──> Control Flow Graph (1000) ─> CFG-GIN ──────────────> z_cfg     (128d)
       │                                                                               │
       └── Execution Trace ─> Syscall Sequence (512) ───> Syscall Bi-LSTM ──────> z_syscall (128d)
                                                                                       │
                                                        [Contrastive & GRAM Alignment] │
                                                                                       ▼
                                                        [Attention Weighted Fusion] ───> z_fused (128d)
                                                                                       │
                                                                                       ▼
                                                                             [Malware Classifier]
                                                                                       │
                                                                                       ▼
                                                                          P(Malware) & Triage Decision
```

---

## 2. Modality Encoders

### 2.1 Opcode Transformer Encoder (`OpcodeTransformer`)
- Processes linear instruction sequences with multi-head self-attention.
- **Layers:** 4 Transformer encoder layers.
- **Hidden Dimension:** $d_{\text{model}} = 128$, feedforward hidden dimension $d_{\text{ff}} = 256$.
- **Attention Heads:** 4.
- **Parameters:** 394,240.

### 2.2 Control Flow Graph GIN (`CFGGIN`)
- Aggregates structural graph topology using Graph Isomorphism Network (GIN) layers.
- **Layers:** 3 GIN layers with Batch Normalization and ReLU non-linearities.
- **Node Input Dimension:** 16.
- **Hidden Dimension:** 128.
- **Parameters:** 26,880.

### 2.3 System Call Bi-LSTM (`SyscallBiLSTM`)
- Models dynamic chronological invocation dependencies.
- **Layers:** 1 Bidirectional LSTM layer ($64 \times 2 = 128$ dimensions).
- **Embedding Dimension:** 64.
- **Parameters:** 99,328.

---

## 3. Contrastive and Geometric Loss Formulation

During joint training, embeddings are aligned in a shared hyperspherical representation space $\mathcal{S}^{d-1}$:

### 3.1 Multi-Modal InfoNCE Loss
For positive modality pair $(z_i^m, z_i^k)$ of the same binary sample $i$:

$$\mathcal{L}_{\text{InfoNCE}}(z^m, z^k) = -\sum_{i=1}^B \log \frac{\exp(\text{sim}(z_i^m, z_i^k) / \tau)}{\sum_{j=1}^B \exp(\text{sim}(z_i^m, z_j^k) / \tau)}$$

where $\text{sim}(u, v) = \frac{u^\top v}{\|u\|_2 \|v\|_2}$ is cosine similarity and $\tau = 0.07$ is the temperature parameter.

### 3.2 Volumetric GRAM Loss
To prevent dimensional collapse and ensure cross-modal geometric dispersion, the Gram matrix $G \in \mathbb{R}^{3 \times 3}$ is constructed from normalized modality vectors $G_{mk} = \text{sim}(z^m, z^k)$. The Volumetric GRAM loss is defined as:

$$\mathcal{L}_{\text{GRAM}} = -\log(\det(G + \epsilon I)) + \lambda_{\text{sep}} \cdot \mathcal{R}_{\text{sep}}$$

where $\lambda_{\text{sep}} = 0.10$ enforces inter-modal separation.

### 3.3 Total Joint Objective

$$\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{BCE}}(y, \hat{y}) + \gamma \cdot \mathcal{L}_{\text{InfoNCE}} + \beta \cdot \mathcal{L}_{\text{GRAM}}$$

with default hyperparameters $\gamma = 0.50, \beta = 1.0, \lambda_{\text{sep}} = 0.10$.

---

## 4. Availability-Aware Attention Late Fusion

When dynamic analysis timeouts or anti-sandbox evasions occur, dynamic system calls are absent ($m_{\text{sy}} = 0$).

The attention fusion layer computes dynamic weights:

$$e_m = \mathbf{w}^\top \tanh(W_m z_m + b_m)$$

The normalized weights $\alpha_m$ are computed via masked softmax:

$$\alpha_m = \frac{\exp(e_m) \cdot m_m}{\sum_{k \in \{\text{op}, \text{cfg}, \text{sy}\}} \exp(e_k) \cdot m_k}$$

The fused latent representation is:

$$z_{\text{fused}} = \sum_m \alpha_m z_m$$

This enables the model to dynamically reallocate attention to static representations (Opcode and CFG) without catastrophic accuracy degradation.
