<!--
reps: 0
priority: 0
-->
#Databases/SQL #SystemDesign/Performance #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**Walk through diagnosing a slow query.**

Don't start with 'add an index'. (1) EXPLAIN ANALYZE (BUFFERS). (2) Worst node; estimate vs actual rows. (3) Sargability. (4) Missing/wrong index, covering. (5) Join type / fan-out. (6) Sort/hash spill. (7) Locks / idle-in-tx. (8) N+1 in the app. Re-EXPLAIN after the change.

**Slow query on ClickHouse?**

query_log read_rows, EXPLAIN indexes=1, parts count, FINAL, JOIN size, missing PK prefix, skip index type mismatch. Adding a Postgres-style B-tree is not an option.
