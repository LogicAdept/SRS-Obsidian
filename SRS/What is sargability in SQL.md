<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**What is a sargable predicate?**

Search ARGument ABLE: the engine can seek a B-tree range instead of computing a value per row. Bare column vs constant/range: col = ?, col BETWEEN, col LIKE 'pre%'. Non-sargable: function/arithmetic/cast on the column, LIKE '%x%', NOT IN with NULLs. Confirm: Index Cond vs Filter in EXPLAIN.

**Sargability analog in ClickHouse?**

Functions on the ORDER BY column block sparse skip (toDate(ts) vs ts range). Same idea: keep the key bare. Skip indexes also require supported functions (hasToken vs lower(LIKE)).
