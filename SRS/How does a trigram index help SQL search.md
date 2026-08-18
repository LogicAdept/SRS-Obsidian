<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/Indexes #Databases/Relational/PostgreSQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**How does pg_trgm make LIKE '%x%' indexable?**

Split strings into overlapping 3-grams. GIN/GiST gin_trgm_ops answers similarity, ILIKE, and regex by intersecting trigram postings. Write-heavier than B-tree. Useless for 1–2 character needles (too few trigrams). EXPLAIN should show Bitmap Index Scan / Index Scan on the GIN, not Seq Scan + Filter.
