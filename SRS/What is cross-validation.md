<!--
reps: 0
priority: 0
-->
#MachineLearning/Metrics #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**What is k-fold cross-validation?**

Split into k folds; train on k-1, validate on 1; rotate; average. Lower-variance estimate than one split when data is small. Stratified k-fold for classification. Time series: use time-aware splits, not shuffled k-fold. Nested CV if you tune hyperparameters.
