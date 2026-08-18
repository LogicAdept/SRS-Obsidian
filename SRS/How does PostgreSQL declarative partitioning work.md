<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/Partitioning #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**How does table partitioning work in Postgres?**

Declarative PARTITION BY RANGE/LIST/HASH. Planner prunes partitions if the WHERE matches the key (don't wrap the key in functions). Maintenance: detach/drop old ranges. Not the same as sharding (still one instance). Constraint exclusion / enable_partition_pruning.
