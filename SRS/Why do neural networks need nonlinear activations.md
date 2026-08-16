<!--
reps: 0
priority: 0
-->
#MachineLearning/DeepLearning #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**Why not stack linear layers only?**

Composition of linear maps is linear. Nonlinearities (ReLU, GELU, sigmoid, tanh) let the net approximate nonlinear functions. Sigmoid/tanh saturate → vanishing grads; ReLU is default hidden; GELU in transformers. Output activation depends on task (sigmoid, softmax, none).
