<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**Why can OR disable a good index?**

Planner may seq-scan or bitmap-OR several indexes. If one side is non-sargable, the whole OR may degrade. Rewrite as UNION of indexed predicates. AND of two selective columns → composite or bitmap AND. Measure; don't assume OR is free.
