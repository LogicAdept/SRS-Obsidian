<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**What is a HOT update?**

Heap-Only Tuple: new version on the same page, no new index entries, if (1) free space on the page and (2) no indexed column changed. fillfactor < 100 leaves room. Indexing every column (or expression indexes on JSONB) kills HOT → write amplification, extra WAL, more vacuum. Interview favorite.
