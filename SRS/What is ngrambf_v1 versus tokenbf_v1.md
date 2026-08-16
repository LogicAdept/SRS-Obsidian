<!--
reps: 0
priority: 0
-->
#Databases/ClickHouse #Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**N-gram bloom vs token bloom?**

ngrambf_v1: overlapping n-grams → substring / LIKE '%x%'. tokenbf_v1: tokens split on non-alphanumerics → hasToken, word LIKE. Both granule-level, false positives, need tuning. From CH 26.2, text inverted index is recommended for FTS; these remain in old tables. Interview: name the query function that matches the index type.
