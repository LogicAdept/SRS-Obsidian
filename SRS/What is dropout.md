<!--
reps: 0
priority: 0
-->
#MachineLearning/Regularization #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**What is dropout?**

Train-time random zeroing of units (or residual streams); approximate an ensemble. Disabled at eval (scale weights). Helps overfitting in big nets. Less used inside modern transformers (drop path / attention dropout instead). Don't use as the only regularizer on tiny data.
