<!--
reps: 0
priority: 0
-->
#Java/Language #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**EXPLAIN ANALYZE.**

EXPLAIN — план без выполнения. EXPLAIN ANALYZE — реальное выполнение + actual time. Seq Scan на большой таблице — плохо. Index Scan / Index Only Scan — хорошо. Rows Removed by Filter — индекс не помогает. estimated ≠ actual rows — нужен ANALYZE.

**EXPLAIN ANALYZE.**

Seq Scan, Index Scan, Bitmap Heap Scan. Nested Loop vs Hash Join. Rows Removed by Filter. estimated vs actual rows.

**EXPLAIN ANALYZE.**

Seq Scan (плохо на большой таблице), Index Scan (хорошо), Bitmap Heap Scan. Rows Removed by Filter — индекс не помогает. estimated ≠ actual → ANALYZE.

**Estimate vs actual?**

ANALYZE runs the query. Huge estimate error → ANALYZE/stats target. Enable track_io_timing if needed.

**Reading a plan for interviews?**

Inner nodes produce rows; actual time × loops. Filter after scan = sargability miss. Hash/Sort memory. Don't optimize estimated cost in isolation.
