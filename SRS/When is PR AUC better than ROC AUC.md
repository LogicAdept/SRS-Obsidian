<!--
reps: 0
priority: 0
-->
#MachineLearning/Metrics #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**When is the precision-recall curve better than ROC?**

Rare positives: FPR stays tiny even with many FPs because TN dominate. PR curve uses precision vs recall and shows the false-alarm cost. Fraud/disease screening: report PR-AUC and precision at a recall target, not just ROC-AUC.
