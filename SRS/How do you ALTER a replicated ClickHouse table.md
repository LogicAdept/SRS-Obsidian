<!--
reps: 0
priority: 0
-->
#Databases/ClickHouse #Databases/Replication #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**ON CLUSTER schema changes?**

ALTER on one replica is queued via Keeper to others. ON CLUSTER for all shards. Mutations (UPDATE) are the dangerous ALTERs. ADD INDEX / MATERIALIZE INDEX for skip/text indexes after the fact — old parts need materialization.
