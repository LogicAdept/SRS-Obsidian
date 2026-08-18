<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #SystemDesign/Performance #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**Why avoid JOINs?**

Distributed hash JOINs shuffle/build large right sides → memory/OOM. Wide facts with dimensions copied at ingest. Dictionaries for small dim lookups (dictGet). ASOF JOIN for time-series alignment. Star schema like Postgres is often the wrong default.
