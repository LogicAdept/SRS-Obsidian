<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/Indexes #NoSQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**SQL FTS vs Elasticsearch?**

Stay in SQL: modest corpus, transactional consistency, ops simplicity, pg_trgm/FTS enough. Move out: typo-tolerant product search, facets, relevance labs, huge write+search QPS, multilingual analyzers. Dual-write/sync lag is the cost. Interview: don't jump to ES for prefix autocomplete on a 10k-row table.

**ClickHouse text index vs ES?**

CH text index: token filter + aggregate in place. ES: relevance, fuzzy, highlighting. Observability stacks sometimes keep both; ClickStack pushes more search into CH.
