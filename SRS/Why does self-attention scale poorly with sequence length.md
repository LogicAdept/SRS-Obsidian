<!--
reps: 0
priority: 0
-->
#MachineLearning/DeepLearning/Transformers #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**Why is attention O(n²)?**

n×n score matrix (and usually materializing it). Long context blows memory. Mitigations: FlashAttention (fused, IO-aware, doesn't store full matrix), sparse/linear attention, sliding window, chunking. KV cache is for decode, not for this quadratic train cost.
