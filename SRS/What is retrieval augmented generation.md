<!--
reps: 0
priority: 0
-->
#MachineLearning/LLM #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**What is RAG?**

Retrieve chunks (usually embeddings + vector DB) and put them in the prompt so the model grounds answers. Cheaper to update than fine-tune, more auditable. Failures: bad chunking, low recall@k, noisy context, model ignoring context. Evaluate retrieval and generation separately (faithfulness vs context precision).
