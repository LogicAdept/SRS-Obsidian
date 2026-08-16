<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**Join types vs join methods?**

INNER/LEFT/RIGHT/FULL/CROSS are logical. Nested loop/hash/merge are physical. Interview: don't confuse LEFT JOIN with a slower method — missing indexes are the usual cost.
