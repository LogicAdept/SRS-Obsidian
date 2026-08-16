<!--
reps: 0
priority: 0
-->
#Databases/ClickHouse #Databases/Replication #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**How does Distributed work?**

No data: fan-out SELECT to shards, merge on coordinator; INSERT by sharding key. Local tables are ReplicatedMergeTree. internal_replication=true: write one replica, let replication copy. Sharding key: even load; for Replacing, keep the same ORDER BY on one shard.
