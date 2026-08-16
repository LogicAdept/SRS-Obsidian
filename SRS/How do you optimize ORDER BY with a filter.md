<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**Index for WHERE + ORDER BY?**

Composite (filter_eq_cols..., sort_cols). Equality first, then the ORDER BY column. Partial index WHERE status='open' (created_at DESC) for a queue. If the filter is not in the index, you sort a huge heap. LIMIT then can stop early only if the index order matches.
