<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**What is a correlated subquery?**

Inner query references outer row → conceptually re-executes per outer row. Optimizers often rewrite to a join, but not always. Classic slow: WHERE col = (SELECT MAX.. WHERE parent_id = outer.id) on a large outer. Rewrite: JOIN to a grouped subquery, window ROW_NUMBER, or LATERAL ... LIMIT.
