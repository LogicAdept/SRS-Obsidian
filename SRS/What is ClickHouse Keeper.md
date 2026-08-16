<!--
reps: 0
priority: 0
-->
#Databases/ClickHouse #Databases/Replication #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**Keeper vs ZooKeeper?**

C++ ZooKeeper-protocol service bundled with CH. Metadata, leader, replication queue, insert hashes. Replacing JVM ZK as the default since ~23.x. Without Keeper there is no ReplicatedMergeTree cluster.
