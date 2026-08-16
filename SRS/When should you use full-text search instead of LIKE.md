<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**When is FTS better than LIKE?**

Natural language: documents, stemming, ranking, language config, boolean queries. LIKE/ILIKE: codes, emails, exact fragments, admin filters. '%word%' on millions of rows is the wrong default. FTS misses substrings inside tokens; trigram covers fuzzy/substring. Elasticsearch when you need facets, typo-tolerance, and a separate cluster.
