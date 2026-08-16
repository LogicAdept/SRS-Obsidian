<!--
reps: 0
priority: 0
-->
#MachineLearning/Regularization #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**What is overfitting and how do you fix it?**

Model memorizes train noise; train loss ↓, val/test loss ↑. Fixes: more data, simpler model, L1/L2, dropout, early stopping, data aug, cross-val. Diagnose the gap first — don't sprinkle dropout on an underfitting model.
