<!--
reps: 0
priority: 0
-->
#MachineLearning/DeepLearning/Transformers #SRS

# Why does self-attention scale poorly with sequence length

> [!abstract] Short answer
> Self-attention computes an **`n × n` score matrix for `n` tokens**: memory and compute grow quadratically — O(n²·d) — while everything else in the transformer is linear in `n`. Doubling the context quadruples attention cost, which is why context windows were 512 tokens for years and why "long context" is an engineering subfield.

The quadratic term is the all-pairs structure: every query must be compared with every key. Feed-forward blocks, embeddings, and the output projections scale linearly — attention dominates as `n` grows. At 2k tokens it is manageable; at 128k it is the entire budget.

## The cost, concretely

```text
scores: n x n x d_k  multiply-adds   -> O(n^2 d)
matrix stored for backward           -> O(n^2) memory
```

**Listing 1.** Both the FLOPs and the training-time memory hit are quadratic — memory often bites first, since the score matrix must be kept for backpropagation: [[What is backpropagation]].

```d2
direction: right
n1: "n = 512\nscore matrix: 262k pairs" { width: 210; height: 80 }
n2: "n = 2k\nscore matrix: 4.2M pairs" { width: 200; height: 80 }
n3: "n = 128k\nscore matrix: 16.4B pairs" { width: 220; height: 80 }
n1 -> n2 -> n3
```

**Fig. 1.** Sixteen times the tokens at the last step means sixty-four thousand times the pairs — the quadratic wall that long-context engineering attacks.

## The mitigation toolbox

* **Exact with better constants:** FlashAttention — tiles the computation, computes softmax in blocks without materializing the n×n matrix in HBM; same math, drastically less memory traffic.
* **Sparse/local patterns:** sliding windows (Longformer), block-sparse attention — most token pairs contribute little anyway.
* **Low-rank/linear approximations:** Performer, Linformer — approximate the score matrix in O(n).
* **Compression:** prefix/anchor tokens, retrieval over long history instead of full attention: [[What is retrieval augmented generation]].
* **KV-cache pressure at inference:** the cache grows linearly with n and multiplies by batch — grouped-query attention and quantized caches are the standard relief: [[What is the KV cache in LLM inference]].

> [!warning] Interview trap
> "FlashAttention makes attention linear." It does not — asymptotics stay O(n²); it removes the memory-materialization bottleneck and improves constants, a different claim entirely. Second trap: "just chunk the text" — naive chunking loses cross-chunk dependencies; sliding windows and retrieval exist precisely because cutting pairs cuts information.

> [!tip] Interview answer
> Attention is O(n²) in both compute and training memory because every token pair gets a score, while the rest of the transformer is linear — so long contexts hit a hard wall. The fixes are exact-but-tiled kernels like FlashAttention, sparse and sliding-window patterns, linear approximations, and retrieval for long histories. At inference the growing KV cache is the parallel concern, handled by grouped-query attention and cache quantization.

