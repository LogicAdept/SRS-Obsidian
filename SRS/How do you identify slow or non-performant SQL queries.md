<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**How do you find slow SQL in production?**

Slow log / pg_stat_statements / performance_schema. Rank by total time not mean. Then EXPLAIN ANALYZE the normalized query. Watch N+1 in APM, not only one fat SQL.
