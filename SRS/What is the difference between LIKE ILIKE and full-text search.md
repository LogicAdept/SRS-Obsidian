<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/Indexes #Databases/PostgreSQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**LIKE vs ILIKE vs FTS?**

LIKE: pattern, case-sensitive in Postgres, '_' / '%'. ILIKE: case-insensitive LIKE, same index rules unless lower() expression index or pg_trgm. FTS: tokenize, stem, stop-words, @@ query, rank; GIN on tsvector. FTS will not find 'phone' inside 'telephone' the way LIKE '%phone%' does. Different tools.
