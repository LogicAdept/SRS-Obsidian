<!--
reps: 0
priority: 0
-->
#Databases/SQL #SystemDesign/Performance #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**What is N+1 at the SQL/ORM boundary?**

1 query for a list + N queries for children. Fix: JOIN, IN/ANY batch, SELECT ... WHERE id = ANY(:ids), ORM fetch join / entity graph. Watch cartesian product after JOIN. SQL interview: show one batched query, then mention covering indexes on (parent_id, ...).
