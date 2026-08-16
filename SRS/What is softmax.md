<!--
reps: 0
priority: 0
-->
#MachineLearning/DeepLearning #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**What is softmax?**

Maps logits to a probability simplex: exp(z_i)/Σexp(z_j). Numerically: subtract max logit. Temperature in LLMs is softmax(z/T). Not used for multi-label (that's independent sigmoids).
