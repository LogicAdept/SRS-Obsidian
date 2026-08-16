<!--
reps: 0
priority: 0
-->
#MachineLearning/MLOps #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**What is data leakage?**

Training uses information not available at prediction time → optimistic metrics, production crash. Classic: scaler/PCA/feature selection fit on full data before split; target-derived features; future timestamps; same user in train and test. Split first, fit preprocessors on train only. Suspiciously perfect AUC → look for leakage.
