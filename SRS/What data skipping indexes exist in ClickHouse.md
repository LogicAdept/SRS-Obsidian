<!--
reps: 0
priority: 0
-->
#Databases/ClickHouse #Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**minmax vs set vs bloom vs text?**

Extra skip indexes on columns not in ORDER BY. minmax: ranges (timestamps, ids in a sorted-ish block). set(N): equality, low cardinality. bloom_filter: equality/IN, high cardinality, false positives. ngrambf_v1 / tokenbf_v1: substring/token (legacy FTS). text: inverted index (GA ~26.2, preferred for token search). GRANULARITY N = one index granule per N table granules.
