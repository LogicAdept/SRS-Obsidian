<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/Replication #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**SharedMergeTree vs ReplicatedMergeTree?**

Cloud: parts in object storage, Keeper for metadata, stateless compute scale-out. Self-host ReplicatedMergeTree on local disks for lowest latency. Elastic replicas without copying data is the Cloud pitch.
