<!--
reps: 0
priority: 0
-->
#MachineLearning/MLOps #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**What is data drift vs concept drift?**

Data/covariate drift: P(X) changes. Concept drift: P(y|X) changes. Both silently kill production accuracy. Monitor input distributions (PSI, embedding drift), labels if you get them, and business metrics. Retrain or alert. Unmonitored model is a liability.
