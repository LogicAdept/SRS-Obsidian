<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/Indexes #Databases/NoSQL/Elasticsearch #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**CH FTS vs Elasticsearch?**

Stay in CH: token filter then aggregate billions of events, one system, ClickStack/logs. ES: relevance, fuzzy/typo UX, facets, highlighting, phrase ranking. CH text index is not a search product. Dual-write if you need both analytics and search UX.
