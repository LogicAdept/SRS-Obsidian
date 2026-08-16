<!--
reps: 0
priority: 0
-->
#MachineLearning/LLM #MachineLearning/Metrics #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Machine Learning (2026). Не сверен с учебниками/статьями. Не считать ответом для ревью.

**How do you evaluate LLM quality?**

No single MSE. Mix: task metrics (EM/F1, pass@k, schema validity), RAGAS-style faithfulness/relevance, LLM-as-judge, human prefs, safety tests. Hold out a golden set. BLEU/ROUGE are weak for open chat. Measure cost/latency too. For RAG split retrieval vs generation.
