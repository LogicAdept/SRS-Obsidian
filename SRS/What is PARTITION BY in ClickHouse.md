<!--
reps: 0
priority: 0
-->
#Databases/ClickHouse #Databases/Partitioning #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**PARTITION BY vs ORDER BY?**

PARTITION BY = lifecycle folders (usually toYYYYMM(ts)): DROP PARTITION, TTL, prune whole months. Not a substitute for ORDER BY skip. Too many partitions (daily × high cardinality) → too many parts, merge pain. Interview: partitions manage data; ORDER BY accelerates filters.
