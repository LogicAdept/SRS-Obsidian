<!--
reps: 0
priority: 0
-->
#MachineLearning/LLM #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**What does temperature do?**

Scales logits before softmax. T→0: greedy/deterministic. T high: flatter, more diverse, more hallucination risk. Factual tasks: 0–0.3. Creative: higher. top-p / top-k truncate the tail. Not a substitute for RAG on facts.
