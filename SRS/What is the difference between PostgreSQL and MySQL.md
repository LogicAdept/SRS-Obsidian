<!--
reps: 0
priority: 0
-->
#Databases/PostgreSQL #Databases/MySQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**Postgres vs MySQL interview?**

Both MVCC OLTP. Postgres: process-per-connection, heap versions + VACUUM, richer types/indexes (JSONB, GIN, arrays), stricter SQL, SSI. InnoDB: undo log, clustered PK, different isolation defaults (RR). Replication/ops differ. Don't claim one is 'just faster'.
