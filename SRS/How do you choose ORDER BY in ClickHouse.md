<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**How do you pick the sorting key?**

Put columns you filter in WHERE as a left prefix (same idea as composite B-tree, different structure). Typical: (user_id, ts) or (date, user_id) matching the dashboard. Low-cardinality first among prefix columns helps compression and skip. Wrong leading column = full granule scan. One table, one ORDER BY — extra access paths = projections or extra MV/tables.
