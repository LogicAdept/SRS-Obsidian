<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**How can a type mismatch disable an index?**

Comparing varchar_id = 123 (or uuid = text) may cast the column, not the literal → seq scan. Match types: bind the same type as the column. Classic: numeric PK vs quoted string; JSON text vs jsonb; timestamptz vs timestamp. EXPLAIN shows a cast in Filter.
