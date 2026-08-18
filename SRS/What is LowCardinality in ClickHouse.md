<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**When do you use LowCardinality(String)?**

Dictionary encoding for few distinct values (country, status, event_type). Less RAM, faster GROUP BY/filter. Harmful if cardinality is huge (unique ids) — dictionary overhead. Not an index; still put frequent filters in ORDER BY or a skip index.
