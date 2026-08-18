<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**How do you drop unused indexes?**

pg_stat_user_indexes.idx_scan = 0 (after enough uptime) plus size. Unique/PK still needed. Unused indexes cost writes, WAL, cache. Replica stats are per-node. Don't drop after a 5-minute restart.

**Drop unused search indexes?**

idx_scan=0 after real traffic. Unique/PK stay. Duplicate trigram + btree on the same column is a common leftover. Writes still pay.
