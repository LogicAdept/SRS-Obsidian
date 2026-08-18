<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**How does Postgres FTS work?**

to_tsvector / to_tsquery (or websearch_to_tsquery). Dictionaries stem and stop-words. GIN (or GiST) on tsvector. Ranking ts_rank. Not Elasticsearch: language config, no distributed relevance at web scale. pg_trgm is a different tool (similarity / ILIKE).

**FTS vs LIKE recap?**

tsvector/tsquery, dictionaries, GIN, ranking. Word search, not '%substr%'. Combine with filters via btree_gin or a separate B-tree + bitmap AND. Language config matters.
