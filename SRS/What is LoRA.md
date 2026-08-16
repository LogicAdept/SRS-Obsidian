<!--
reps: 0
priority: 0
-->
#MachineLearning/LLM #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**What is LoRA?**

Low-Rank Adaptation: freeze base weights, train small rank-decomp matrices in attention/MLP. Cheap PEFT. Merge adapters or swap per tenant. Not a retrieval system. QLoRA: quantized base + LoRA for smaller GPUs.
