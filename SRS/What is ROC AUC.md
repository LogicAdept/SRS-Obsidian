<!--
reps: 0
priority: 0
-->
#MachineLearning/Metrics #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**What is ROC-AUC?**

ROC: TPR vs FPR as you sweep threshold. AUC: P(score_positive > score_negative) for a random pair. Threshold-free ranking metric. Looks good under heavy imbalance even if precision is useless — then use PR-AUC. Not a substitute for a chosen operating point.
