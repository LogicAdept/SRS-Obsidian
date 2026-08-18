<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #SystemDesign/Performance #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**Slow CH query checklist?**

EXPLAIN indexes=1 / PLAN. system.query_log: read_rows vs result. PK prefix? partition prune? skip/text index type match? too many parts? FINAL? JOIN of a huge table? SELECT fat columns? PREWHERE. Then ORDER BY/projection/MV, not a Postgres-style CREATE INDEX on every column.
