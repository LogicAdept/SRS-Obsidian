<!--
reps: 0
priority: 0
-->
#Databases/ClickHouse #Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**What is a granule / index_granularity?**

Default 8192 rows: the skip unit of the sparse index. primary.idx stores the ORDER BY key of the first row of each granule. Query reads whole granules that might match — not row-level B-tree seeks like Postgres. Smaller granularity → bigger index, finer skip.
