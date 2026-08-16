<!--
reps: 0
priority: 0
-->
#MachineLearning/DeepLearning #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**Why does initialization matter?**

Too large → explode; too small → vanish. Xavier/Glorot for tanh/sigmoid; He/Kaiming for ReLU. Transformers: residual-aware init. All-zero weights (except some biases) prevent symmetry breaking. Interview: init is part of why BatchNorm/residual nets train.
