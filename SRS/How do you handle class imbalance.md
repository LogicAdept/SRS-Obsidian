<!--
reps: 0
priority: 0
-->
#MachineLearning/Metrics #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**How do you handle class imbalance?**

Don't trust accuracy. Use PR-AUC, F1, recall@precision. Class weights / focal loss. Threshold tuning on val. Sampling (undersample majority, SMOTE) is a tool, not magic — can leak if done before split. Collect more minority data if you can. Cost of FN vs FP drives the metric.
