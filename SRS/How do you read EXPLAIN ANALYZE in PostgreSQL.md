<!--
reps: 0
priority: 0
-->
#Databases/PostgreSQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**EXPLAIN vs EXPLAIN ANALYZE?**

EXPLAIN: planner estimate only. ANALYZE: actually runs (wrap DML in BEGIN; ROLLBACK). BUFFERS: hits/reads. Read inner nodes first; look at actual time, loops (Nested Loop × inner), rows estimated vs actual. Seq Scan on big table, Sort that spills, Hash that exceeds work_mem. Enable pg_stat_statements.

**Postgres plan reading for SQL opt?**

ANALYZE+BUFFERS. Heap Fetches on IOS. Bitmap Heap. work_mem batches. Rows Removed by Filter → better index or rewrite LIKE/function.
