<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/SQL/DDL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**How do you ALTER a huge table online?**

PG 11+: ADD COLUMN with constant default is metadata-only (no rewrite). Volatile default still rewrites. NOT NULL on 100M rows: add nullable, batch backfill, ADD CONSTRAINT NOT VALID, then VALIDATE. CREATE INDEX CONCURRENTLY. lock_timeout so you don't queue behind a long tx. ACCESS EXCLUSIVE is the outage lock.
