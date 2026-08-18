<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/OLAP/Druid #Databases/OLAP/Pinot #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**ClickHouse vs Druid vs Pinot?**

All real-time OLAP. CH: richest SQL, simple ops, scans+skip indexes. Druid: streaming ingest + tiered segments. Pinot: star-tree, ultra-low-latency user-facing. Interview: don't claim one always wins.
