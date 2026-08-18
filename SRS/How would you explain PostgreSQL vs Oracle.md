<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/Relational/Oracle #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**PostgreSQL vs Oracle — ключевые отличия.**

PG: SERIAL/IDENTITY (автоинкремент), LIMIT/OFFSET, нет Read Uncommitted. Oracle: SEQUENCE, ROWNUM / FETCH FIRST N ROWS, NVL вместо COALESCE, DUAL для SELECT без таблицы, CONNECT BY для иерархий. В PG Repeatable Read решает phantom reads (MVCC).

**Postgres vs Oracle interview?**

Postgres: MVCC heap versions + VACUUM. Oracle: undo. Licensing vs OSS. Sequences/identity, partitioning, JSONB vs JSON in Oracle. Skills transfer; vacuum/bloat is the Postgres-specific ops story.
