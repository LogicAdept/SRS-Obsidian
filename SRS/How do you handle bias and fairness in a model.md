<!--
reps: 0
priority: 0
-->
#MachineLearning/MLOps #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**How do you handle bias and fairness?**

Audit data and labels, slice metrics by group before launch, document (model card), monitor drift of slices. Bias is not only 'imbalanced classes'. No single fairness metric; pick constraints with legal/product. Retrain as the world changes.
