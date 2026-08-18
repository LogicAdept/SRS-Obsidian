<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #SystemDesign/Performance #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**When is ClickHouse the wrong tool?**

High-concurrency point OLTP, multi-row ACID, frequent row UPDATE/DELETE, JOIN-heavy 3NF schemas, relevance search UX. Mutations and FINAL are not workarounds that make it Postgres. HTAP: Postgres + CDC (PeerDB/Debezium) → CH.
