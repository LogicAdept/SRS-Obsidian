<!--
reps: 0
priority: 0
-->
#MachineLearning/Optimization #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**What is hyperparameter tuning?**

Hyperparameters (lr, depth, C, k) are set before training, not learned. Search on validation: grid, random (often better in high-D), Bayesian. Nested CV if you report a number. Don't tune on the test set. Early stopping is a hyperparameter too.
