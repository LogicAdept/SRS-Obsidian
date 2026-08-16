<!--
reps: 0
priority: 0
-->
#MachineLearning/Metrics #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**Train vs validation vs test?**

Train: fit parameters. Validation: model/hyperparameter choice (can leak if reused a lot). Test: final unbiased estimate — touch rarely. Typical 70/15/15 or 80/10/10. Imbalance → stratify. Time series → chronological, not random shuffle.
