<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/Indexes #Databases/PostgreSQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**Index Cond vs Filter?**

Index Cond: used as a seek/scan key inside the index. Filter: leftover predicate applied to rows after the index (or heap) — extra work, Rows Removed by Filter. If Filter is huge, extend the index (composite / INCLUDE) or rewrite to be sargable so it becomes Index Cond.
