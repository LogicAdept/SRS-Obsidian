<!--
reps: 0
priority: 0
-->
#MachineLearning/Supervised #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**How does k-nearest neighbors work?**

Lazy: no real training. Predict from k closest train points (majority / mean). Needs a distance; scale features. Slow predict O(n); KD-tree/HNSW/ANN for speed. Curse of dimensionality. k small → variance; k large → bias. Not great on huge sparse data.
