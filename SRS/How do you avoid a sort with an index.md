<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**How can an index satisfy ORDER BY?**

B-tree already ordered. Index (user_id, created_at DESC) can filter user_id and return rows in created_at order — no Sort node. Mixing ASC/DESC must match the index (or use NULLS LAST variants). Extra SELECT columns may still need heap lookups unless covering.
