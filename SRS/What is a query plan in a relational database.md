<!--
reps: 0
priority: 0
-->
#Databases/SQL #SystemDesign/Performance #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**What is a query plan?**

Tree of scans, joins, sorts, aggregates the optimizer chose by estimated cost. EXPLAIN shows it; ANALYZE adds actuals. Wrong stats → wrong plan. Cost units are not milliseconds.

**ClickHouse EXPLAIN?**

EXPLAIN / EXPLAIN indexes=1 / PLAN. Look at granule marks read, skip indexes, pipeline. Cost model differs from PG; skipping is the main 'index used' signal.
