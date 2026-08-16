<!--
reps: 0
priority: 0
-->
#Databases/ClickHouse #Databases/Replication #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**How does replication dedup inserts?**

Keeper/ZooKeeper: replication log, block hashes. Same insert block hash → dropped (block-level exactly-once for retries). Quorum settings exist. ALTER ON CLUSTER / one-replica ALTER queued. Lag: system.replication_queue, merges starved during backfill.
