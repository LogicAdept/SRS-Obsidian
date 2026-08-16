<!--
reps: 0
priority: 0
-->
#MachineLearning/DeepLearning/Transformers #MachineLearning/DeepLearning/RNN #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**Why transformers over RNNs/LSTMs?**

Self-attention: every token attends to every other in parallel → GPU-friendly, better long-range deps. No recurrence bottleneck. Cost: O(n²) attention memory/time in naive form. Positional encodings inject order. This is why LLMs are transformer stacks.
