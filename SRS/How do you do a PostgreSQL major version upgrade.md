<!--
reps: 0
priority: 0
-->
#Databases/PostgreSQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**pg_upgrade vs logical replication upgrade?**

pg_upgrade (hard links) is fast with downtime. Dump/restore is slow. Near-zero: logical replication to a new major, catch up, cut over. Replicas must match major for physical streaming. Extensions/slots/C functions are the gotchas. Test on a copy.
