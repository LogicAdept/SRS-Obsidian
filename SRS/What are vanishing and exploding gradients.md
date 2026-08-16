<!--
reps: 0
priority: 0
-->
#MachineLearning/DeepLearning #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**Why do gradients vanish or explode?**

Many multiplies of |λ|<1 → vanish (can't train early layers / long RNNs). |λ|>1 → explode (NaNs). Fixes: ReLU, residual connections, LSTM/GRU gates, gradient clipping, careful init (Xavier/He), BatchNorm/LayerNorm, skip connections. Transformers still use residuals + norm.
