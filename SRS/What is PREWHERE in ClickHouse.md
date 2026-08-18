<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/SQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**PREWHERE vs WHERE?**

Read cheap/selective columns first, filter, then read fat columns for survivors. CH often infers PREWHERE. Manual PREWHERE: small, highly selective predicate (id, enum), not the 10 MB log body. Complements skip indexes; does not replace ORDER BY design.
