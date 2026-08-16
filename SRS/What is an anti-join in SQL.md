<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**How do you find rows with no match?**

LEFT JOIN ... WHERE right.pk IS NULL, or NOT EXISTS. Prefer NOT EXISTS over NOT IN (NULL). Planner may show Anti Join. Index the lookup key on the right table. Classic: customers without orders.
