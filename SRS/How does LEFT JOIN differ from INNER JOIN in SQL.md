<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**LEFT JOIN optimization gotcha?**

LEFT JOIN ... WHERE right.col = 1 turns into INNER. Filters on the right belong in ON if you meant to keep left rows. Not EXISTS for anti-join. Index both keys.
