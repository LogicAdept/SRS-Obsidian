<!--
reps: 0
priority: 0
-->
#MachineLearning/LLM #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**What is prompt injection?**

User/content tries to override system instructions ('ignore previous...'). RAG docs can contain injections. Mitigate: isolate untrusted text, tool allowlists, output filters, don't put secrets in the prompt. Related to jailbreaks; treat retrieved text as hostile.
