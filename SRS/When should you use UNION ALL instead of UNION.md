<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**UNION vs UNION ALL for speed?**

UNION dedupes (sort/hash) — extra cost. UNION ALL concatenates. If sets are disjoint or duplicates are OK, ALL. Also a rewrite trick: split OR into two indexed UNION ALL branches.
