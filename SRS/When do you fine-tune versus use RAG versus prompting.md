<!--
reps: 0
priority: 0
-->
#MachineLearning/LLM #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**Prompt vs RAG vs fine-tune (LoRA)?**

Start with prompting. RAG when facts must stay current / cited / too big for weights. Fine-tune/LoRA when you need style, format, domain jargon, or the behavior prompting can't lock. LoRA: small adapters, freeze base. Don't fine-tune to 'add yesterday's docs' — that's RAG.
