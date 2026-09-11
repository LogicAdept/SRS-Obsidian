<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Как читать EXPLAIN ANALYZE?**

Смотри на Seq Scan (на большой таблице — плохо), Index Scan, Bitmap Heap Scan, типы Join (Nested Loop vs Hash Join), Rows Removed by Filter, разницу estimated vs actual rows.

**Как прочитать EXPLAIN ANALYZE?**

Обратите внимание на Seq Scan (плохо на больших таблицах), Index Scan, Bitmap Heap Scan, Nested Loop vs Hash Join, Rows Removed by Filter, разницу estimated vs actual rows.

**Postgres EXPLAIN practice?**

EXPLAIN (ANALYZE, BUFFERS). Compare rows. Seq Scan, Nested Loop loops, sort/hash memory. ROLLBACK for writes.

**EXPLAIN vs ANALYZE for optimization?**

EXPLAIN is estimate only. ANALYZE runs it (ROLLBACK DML). Look Seq Scan, Nested Loop loops, Sort spill, rows mismatch. BUFFERS for I/O. Index Cond vs Filter.

EXPLAIN — план без выполнения. EXPLAIN ANALYZE — реальное выполнение + actual time. Seq Scan на большой таблице — плохо. Index Scan / Index Only Scan — хорошо. Rows Removed by Filter — индекс не помогает. estimated ≠ actual rows — нужен ANALYZE.
**Estimate vs actual?**
ANALYZE runs the query. Huge estimate error → ANALYZE/stats target. Enable track_io_timing if needed.
**Reading a plan for interviews?**
Inner nodes produce rows; actual time × loops. Filter after scan = sargability miss. Hash/Sort memory. Don't optimize estimated cost in isolation.
