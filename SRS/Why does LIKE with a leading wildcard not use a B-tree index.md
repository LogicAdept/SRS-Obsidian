<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**Why is LIKE '%smith' a table scan?**

B-tree is ordered like a dictionary: it needs a known prefix to seek. '%smith' / '%x%' hide the start, so every leaf must be checked. LIKE 'smith%' is a prefix range and can Index Scan. _ in the first position is the same trap. Interview pivot: wildcards → then the index story.

**LIKE '%x%' in ClickHouse?**

There is no B-tree seek anyway. Use ngrambf_v1 or a text index with ngram tokenizer, plus a time/service prefix in ORDER BY so you don't scan the whole history. hasToken if it is a word.
