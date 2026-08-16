<!--
reps: 0
priority: 0
-->
#MachineLearning/DeepLearning/Transformers #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**What is a causal mask?**

Decoder LM: token i cannot attend to j>i (future). Implemented as -inf in the score matrix before softmax. Off-by-one mask → train/test mismatch and garbage generation. Encoder bidirectional models (BERT) do not use causal masks.
