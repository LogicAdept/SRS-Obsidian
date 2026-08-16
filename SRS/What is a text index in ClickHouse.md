<!--
reps: 0
priority: 0
-->
#Databases/ClickHouse #Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**What is ClickHouse full-text search?**

Inverted index: token → row/granule postings. Tokenizers (splitByNonAlpha, ngrams, …), optional lower() preprocessor. Functions: hasToken, hasAnyTokens, hasAllTokens; LIKE may use it if tokens extract. Deterministic vs bloom. Not BM25/relevance — filter+aggregate, not Elasticsearch ranking. Observability/logs + GROUP BY is the sweet spot.
