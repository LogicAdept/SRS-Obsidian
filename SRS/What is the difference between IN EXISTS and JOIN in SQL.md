<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**IN vs EXISTS vs JOIN?**

IN (list): small static sets; NULL in NOT IN nukes the result. EXISTS: semi-join, short-circuit, safer for 'any match'. JOIN: when you need columns; can duplicate rows if the match is not 1:1. Modern planners often make IN/EXISTS similar — still prefer EXISTS for correlated 'has child' and NOT EXISTS over NOT IN.
