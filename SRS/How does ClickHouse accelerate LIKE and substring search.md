<!--
reps: 0
priority: 0
-->
#Databases/ClickHouse #Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**LIKE '%foo%' in ClickHouse?**

No B-tree prefix magic like Postgres. Full column scan unless a skip/text index applies. ngrambf_v1: n-grams in a bloom — can skip granules for LIKE '%…%' if the needle ≥ ngram size; probabilistic. text index with ngrams/sparseGrams tokenizer: newer path. hasToken / token index for word search. Don't put a random String in ORDER BY hoping LIKE gets faster.
