<!--
reps: 0
priority: 0
-->
#MachineLearning/Supervised #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**One-hot vs learned embeddings?**

One-hot: sparse high-dim, no notion of similarity, blows up with high cardinality. Embeddings: dense vectors, similar cats close, standard in deep nets and recommenders. Target encoding for trees (leak-safe, out-of-fold). Don't one-hot million IDs into a linear model without hashing.
