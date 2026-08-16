<!--
reps: 0
priority: 0
-->
#MachineLearning/LLM #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**What is an LLM? What is a context window?**

Transformer LM trained on large token corpora to predict next token (or masked tokens). Context window = tokens in one forward (prompt+generation). Longer context helps RAG/reasoning but costs memory (KV cache) and $ per token. Not infinite memory — dump it and quality drops.
