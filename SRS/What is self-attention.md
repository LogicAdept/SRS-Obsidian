<!--
reps: 0
priority: 0
-->
#MachineLearning/DeepLearning/Transformers #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**What is self-attention / QKV?**

Each token → Q, K, V. Scores = QKᵀ / √d_k, softmax, weighted sum of V. 'What to look at' (QK) vs 'what to copy' (V). Multi-head: several subspaces then concat. Causal mask for autoregressive LM (can't see future). Softmax stability: subtract max.
