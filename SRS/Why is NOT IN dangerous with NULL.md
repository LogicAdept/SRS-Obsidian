<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**Why can NOT IN return no rows?**

x NOT IN (a, NULL) is UNKNOWN for every x because NULL comparisons are not TRUE. The WHERE drops all rows. NOT EXISTS / LEFT JOIN ... IS NULL do not have this trap. Interview classic alongside three-valued logic.
