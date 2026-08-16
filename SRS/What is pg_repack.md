<!--
reps: 0
priority: 0
-->
#Databases/PostgreSQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**pg_repack vs VACUUM FULL?**

Online rewrite: compact table/indexes with weaker locking than VACUUM FULL's ACCESS EXCLUSIVE. Still needs disk headroom and a replica-safe window. Not a substitute for fixing autovacuum / long transactions.
