<!--
reps: 0
priority: 0
-->
#MachineLearning/Optimization #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**Adam vs SGD with momentum?**

Adam: per-parameter adaptive LR (first+second moments), fast start, default for transformers. SGD+momentum: often better final generalization on vision if tuned. AdamW decouples weight decay. Interview: Adam is not always 'better'; report both if it matters.
