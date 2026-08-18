<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/Partitioning #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**What is over-partitioning?**

Each partition is a separate part namespace. Thousands of tiny partitions → part explosion, memory for parts, slow merges. Prefer monthly/weekly, not unique user_id as partition. Cardinality of the partition expression should stay small.
