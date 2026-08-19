<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/Indexes/Functional #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**Why does WHERE YEAR(created_at) = 2026 skip the index?**

The index stores raw column values. A function means every row must be transformed before compare — no range seek. Rewrite: created_at >= '2026-01-01' AND created_at < '2027-01-01'. Or an expression index on the function if you cannot rewrite. Same trap: LOWER(email), CAST, DATE(col).
