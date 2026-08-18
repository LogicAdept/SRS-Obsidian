<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**When skip indexes fail?**

Column values mixed in every granule (not correlated with ORDER BY) → bloom always hits. Wrong type (minmax on high-card random strings). GRANULARITY too coarse. Query uses a function the index does not support (ILIKE vs hasToken). Data not yet merged / index not materialized after ADD INDEX.
