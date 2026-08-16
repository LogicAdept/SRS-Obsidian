<!--
reps: 0
priority: 0
-->
#MachineLearning/DeepLearning #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**How does a neural network learn?**

Forward pass → loss vs target → backprop (chain rule) gives ∂L/∂w → optimizer steps weights. Repeat minibatches. Needs nonlinearity between layers or it collapses to one linear map. Generalization is the goal, not zero train loss.
