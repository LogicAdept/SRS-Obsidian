<!--
reps: 0
priority: 0
-->
#MachineLearning/Ensembles #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**What is stacking?**

Train diverse base models, then a meta-learner on their predictions. Use out-of-fold preds to avoid leakage (the meta-train must not see in-sample base preds). Heavier than bagging/boosting; easy to leak if you stack on full-train preds.
