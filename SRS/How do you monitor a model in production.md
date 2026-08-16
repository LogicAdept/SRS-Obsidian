<!--
reps: 0
priority: 0
-->
#MachineLearning/MLOps #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**What do you monitor after deploy?**

Prediction volume, latency, null rates, feature distributions vs train, performance vs delayed labels, fairness slices, cost. For LLMs: toxicity, faithfulness, cache hit rate, tokens. Alert on drift before users scream. Shadow/canary when swapping models.
