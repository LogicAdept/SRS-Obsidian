<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**Why can't WHERE use a SELECT alias?**

Typical logical order: FROM/JOIN → WHERE → GROUP BY → HAVING → SELECT (aliases, windows) → DISTINCT → ORDER BY → LIMIT. WHERE cannot see SELECT aliases; ORDER BY can. Filtering early with WHERE beats HAVING for non-aggregates.
