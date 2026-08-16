<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**Why aggregate before joining?**

Shrink the many-side first so the join is 1:1 and SUM/COUNT stay correct. Derived table / CTE of GROUP BY key. Opposite anti-pattern: join then DISTINCT/GROUP BY to undo duplication.
