<!--
reps: 0
priority: 0
-->
#Databases/ClickHouse #Databases/Partitioning #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**DROP PARTITION vs DELETE?**

DROP PARTITION / TTL DELETE on partition key is metadata-fast. ALTER DELETE mutation rewrites parts. Design PARTITION BY so retention is a partition drop. Search indexes die with the partition — no extra vacuum story like Postgres.
