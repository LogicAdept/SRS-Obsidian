<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**Database is slow at 3am — first five minutes?**

pg_stat_activity (running, idle in transaction, wait_event). Locks. Disk full / IOPS. Replication lag / slot WAL. One query dominating → cancel if safe. Recent migration/deploy. Then pg_stat_statements, not random REINDEX.
