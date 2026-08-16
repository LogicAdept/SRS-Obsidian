<!--
reps: 0
priority: 0
-->
#Databases/PostgreSQL #Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**B-tree vs GIN vs GiST vs BRIN vs hash?**

B-tree: default, = < > BETWEEN ORDER BY, LIKE 'abc%'. Hash: = only. GIN: inverted, JSONB, arrays, FTS. GiST: geometry, ranges, some FTS. BRIN: huge naturally ordered tables (time). SP-GiST: partitioned space. Don't GIN a bigint equality column. INCLUDE covering is B-tree.
