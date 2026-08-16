<!--
reps: 0
priority: 0
-->
#MachineLearning/Optimization #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**Why cross-entropy for classification?**

Negative log-likelihood of the correct class after softmax/sigmoid. Strongly penalizes confident wrong answers. Pair with softmax (multi) or sigmoid (binary/multi-label). MSE on class indices is the wrong default.
