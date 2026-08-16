<!--
reps: 0
priority: 0
-->
#MachineLearning/LLM #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**What is the KV cache and why does it matter?**

Autoregressive decode: without cache you'd recompute K/V for all past tokens every step (O(n²) compute). Cache past K/V → O(n) per new token. Memory bottleneck at long context; PagedAttention/vLLM pages KV. Bug: wrong cache index/positions → garbage text. Prefill vs decode.
