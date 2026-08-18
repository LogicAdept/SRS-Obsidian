<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**VACUUM vs VACUUM FULL vs ANALYZE?**

VACUUM: concurrent, marks dead space reusable, updates FSM/visibility map, freeze; does not shrink file to OS. VACUUM FULL: rewrite table, exclusive lock, compact to OS. ANALYZE: planner stats only. Autovacuum does VACUUM+ANALYZE. Don't FULL in prod without a window; use pg_repack.
