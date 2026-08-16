<!--
reps: 0
priority: 0
-->
#MachineLearning/DeepLearning/RNN #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**What is an RNN / BPTT problem?**

Hidden state updated token-by-token; BPTT unfolds through time. Sequential → hard to parallelize. Long range: vanishing/exploding grads. LSTM/GRU add gates for longer memory, still weaker and slower to train than transformers on language.
