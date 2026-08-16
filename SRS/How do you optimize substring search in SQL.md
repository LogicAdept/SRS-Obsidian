<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/Indexes #SystemDesign/Performance #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**How do you speed up LIKE '%foo%'?**

B-tree cannot. Options: (1) pg_trgm GIN/GiST — trigrams, also ILIKE/regex. (2) Full-text tsvector + GIN — words, stemming, ranking, not arbitrary substrings. (3) Reverse column + LIKE 'htims%' for suffix-only. (4) Dedicated search (OpenSearch) at scale. Don't add 12 B-trees hoping '%x%' gets faster.

**Substring search on CH logs?**

ngrambf / text(ngrams). Still prune by date partition and ORDER BY prefix first. Full-history LIKE '%x%' is a cluster-killer. ES if you need ranking.

**CH vs PG for contains search?**

PG: pg_trgm GIN. CH: ngrambf/text ngrams + time prune. Both still lose to token search when the needle is a word (hasToken / FTS).
