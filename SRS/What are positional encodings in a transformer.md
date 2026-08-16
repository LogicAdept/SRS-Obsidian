<!--
reps: 0
priority: 0
-->
#MachineLearning/DeepLearning/Transformers #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**Why positional encodings?**

Attention is permutation-equivariant without positions. Add/inject position: sinusoids, learned embeddings, RoPE (relative, common in LLMs). Wrong positions at decode (KV cache) → garbage generation. Interview debug favorite.
