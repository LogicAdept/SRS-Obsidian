<!--
reps: 0
priority: 0
-->
#Databases/ClickHouse #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**What is a part?**

One INSERT (or merge result) = a directory: one file per column, marks, sparse primary.idx, checksums. Too many small parts → slow queries and 'Too many parts'. Merges reduce count. Wide parts are the read unit alongside granules.
