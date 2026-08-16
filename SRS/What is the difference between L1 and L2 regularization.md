<!--
reps: 0
priority: 0
-->
#MachineLearning/Regularization #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**L1 vs L2?**

Both add a penalty on weights to the loss. L2 (Ridge): shrinks weights smoothly, keeps all features. L1 (Lasso): sparsity, feature selection. Elastic Net mixes both. Scale features first. Neural nets: weight decay ≈ L2; dropout is a different regularizer.
