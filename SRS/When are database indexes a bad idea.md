<!--
reps: 0
priority: 0
-->
#Databases/Indexes #SystemDesign/Tradeoffs #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**When not to index in Postgres?**

Tiny tables, write-heavy rarely-read, low selectivity alone, unused idx_scan=0. Every index can kill HOT if that column is updated. Measure with pg_stat_statements first.
