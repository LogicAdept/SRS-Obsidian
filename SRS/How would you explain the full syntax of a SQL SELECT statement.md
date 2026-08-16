<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**Clause order vs execution order?**

Written SELECT-FROM-WHERE-GROUP-HAVING-ORDER-LIMIT. Logical: FROM → WHERE → GROUP → HAVING → SELECT → DISTINCT → ORDER → LIMIT. Explains alias and window placement.
