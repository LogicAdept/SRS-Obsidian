<!--
reps: 0
priority: 0
-->
#Databases/PostgreSQL #Databases/ClickHouse #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**Postgres vs ClickHouse?**

Postgres: row store, OLTP, FK, MVCC, point updates. ClickHouse: columnar, OLAP, append-heavy, sparse indexes, weak update/transaction story. Analytics on Postgres hits I/O; OLTP on ClickHouse is the wrong tool. HTAP: often both, not one.

**CH vs PG recap for interviews?**

PG: row, MVCC, B-tree per row, UPDATE, FK. CH: columns, parts/merges, sparse granule index, batch INSERT, mutations expensive. Search: PG GIN/trgm vs CH skip/text indexes. Use both via CDC, not one DB for all.
