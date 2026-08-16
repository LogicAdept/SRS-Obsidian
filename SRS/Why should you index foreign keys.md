<!--
reps: 0
priority: 0
-->
#Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**Why index FK columns?**

Child lookups (WHERE parent_id = ?) and JOIN nested loops need it. ON DELETE CASCADE/SET NULL locks and scans the child — without an index that can be a table lock storm. Most ORMs do not create these indexes for you.
