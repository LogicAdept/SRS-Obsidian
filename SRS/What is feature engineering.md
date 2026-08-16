<!--
reps: 0
priority: 0
-->
#MachineLearning/Supervised #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**What is feature engineering and why does it beat swapping models?**

Turn raw data into signal: ratios, bins, embeddings, target encoding (carefully), domain features. A linear model on good features often beats a fancy model on junk. Fit encodings on train only. When the model is weak, inspect features before jumping to deep learning.
