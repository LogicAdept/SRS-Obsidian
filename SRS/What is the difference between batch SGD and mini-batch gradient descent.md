<!--
reps: 0
priority: 0
-->
#MachineLearning/Optimization #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**Batch vs stochastic vs mini-batch GD?**

Batch: full dataset per step, stable, slow, memory-heavy. SGD: one example, noisy, can escape saddles, noisy updates. Mini-batch: n=32–512, GPU-friendly compromise. 'SGD' in deep learning usually means mini-batch + momentum/Adam.
