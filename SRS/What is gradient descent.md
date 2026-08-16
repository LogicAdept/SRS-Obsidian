<!--
reps: 0
priority: 0
-->
#MachineLearning/Optimization #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**What is gradient descent and why does learning rate matter?**

Iteratively step parameters opposite the gradient of the loss. LR too big → diverge/overshoot; too small → crawl. Mini-batch is the production default (noise + vectorization). Variants: momentum, Adam. Local minima / saddle points in non-convex nets; LR schedules and warmup matter.
