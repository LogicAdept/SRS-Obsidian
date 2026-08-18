<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**What is CREATE INDEX CONCURRENTLY?**

Ordinary CREATE INDEX takes a lock that blocks writes. CONCURRENTLY: two heap scans, slower, allows writes. Failure leaves an INVALID index — drop/reindex before retry. Production default on large tables. Same idea: REINDEX CONCURRENTLY, DROP INDEX CONCURRENTLY.
