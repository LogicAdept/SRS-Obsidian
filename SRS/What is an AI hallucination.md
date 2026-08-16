<!--
reps: 0
priority: 0
-->
#MachineLearning/LLM #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**What is hallucination and how do you reduce it?**

Fluent but false content (facts, citations, consistency). Reduce: RAG + cite-and-verify, lower temperature, constrained decoding/JSON schema, 'say I don't know', self-consistency, LLM-as-judge, human review on low confidence. Zero is not achievable; detect and degrade.
