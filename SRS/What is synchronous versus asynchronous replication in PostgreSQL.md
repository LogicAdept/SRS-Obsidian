<!--
reps: 0
priority: 0
-->
#Databases/PostgreSQL #Databases/Replication #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**Sync vs async replication?**

Async (default): primary commits then ships WAL — RPO>0 if primary dies before replica. Sync: wait for replica flush (synchronous_commit / synchronous_standby_names). Quorum: ANY 2 (...). Finance: sync. Analytics replica: async. Sync costs latency and availability if the standby dies.
