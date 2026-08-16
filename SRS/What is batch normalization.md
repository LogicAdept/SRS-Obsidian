<!--
reps: 0
priority: 0
-->
#MachineLearning/DeepLearning #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**What is batch normalization?**

Normalize activations using batch mean/var, then scale/shift. Speeds training, allows higher LR, some regularization. Train vs eval: running averages. Batch size 1 is painful. LayerNorm/RMSNorm preferred in transformers (no batch axis). Don't mix BN+dropout carelessly.
