<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/OLAP/Snowflake #SystemDesign/Performance #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**ClickHouse vs Snowflake/BigQuery?**

CH: low-latency user-facing analytics, self-host or Cloud, sparse indexes. Snowflake/BQ: warehouse, elasticity, weaker sub-100ms dashboards, scan-priced. Pick by p99 and cost model, not 'both are OLAP'.
