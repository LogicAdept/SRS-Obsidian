<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**How do you debug a slow query?**

pg_stat_statements → EXPLAIN (ANALYZE, BUFFERS) → check estimates, scans, joins, sorts → index/partial/covering, rewrite, ANALYZE, work_mem, vacuum/bloat, lock waits (pg_locks / activity). Don't add 12 indexes blindly. Check idle-in-tx and autovacuum lag.

**Slow query loop?**

statements → EXPLAIN ANALYZE BUFFERS → sargability/index/join/spill/vacuum. Re-check after ANALYZE. Search queries: confirm Index Cond, not Filter on LIKE.

**Don't apply PG vacuum advice to CH?**

CH has no VACUUM/MVCC bloat story. Slow CH is parts, marks, FINAL, JOINs, wrong ORDER BY. Different checklist.
