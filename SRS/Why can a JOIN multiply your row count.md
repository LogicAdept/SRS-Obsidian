<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**Why did SUM explode after a JOIN?**

One-to-many: each left row repeats per match → aggregates double-count. Pre-aggregate the many side to one row per key, then JOIN. Or window + DISTINCT ON / ROW_NUMBER=1 if you needed one child. Check COUNT(*) before vs after the join.
