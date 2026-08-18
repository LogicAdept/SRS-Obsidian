<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**How do you speed up LIKE '%foo%'?**

pg_trgm: trigram GIN/GiST indexes for similarity and ILIKE '%x%'. B-tree only helps prefix LIKE 'x%'. Fuzzy search without Elasticsearch for moderate scale.

**Trigram for LIKE optimization?**

gin_trgm_ops: ILIKE '%x%', similarity, regex. The standard answer when the interviewer shows LIKE '%foo%'. Short patterns and huge write load are the limits.
