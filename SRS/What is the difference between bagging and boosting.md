<!--
reps: 0
priority: 0
-->
#MachineLearning/Ensembles #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**Bagging vs boosting?**

Bagging: parallel models on bootstrap samples, average/vote — mainly cuts variance (Random Forest). Boosting: sequential, each model fits residuals/errors — cuts bias, can overfit if too many rounds (GBDT). Stacking: meta-model on out-of-fold preds. Don't use linear models as weak learners for typical boosting trees.
