<!--
reps: 0
priority: 0
-->
#MachineLearning/DeepLearning/Transformers #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**Why multiple attention heads?**

Heads project into smaller d_k, attend in parallel, concat, linear mix. Different heads can specialize (syntax vs rare tokens). d_k = d_model/h. More heads ≠ always better; too small d_k hurts.
