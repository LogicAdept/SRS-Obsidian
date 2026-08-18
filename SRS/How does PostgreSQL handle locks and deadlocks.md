<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/SQL/Transactions #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**Row locks vs deadlocks?**

Writers take row locks (FOR UPDATE / UPDATE). Readers usually don't (MVCC). Deadlock: two tx lock rows in opposite order → one aborted (40001). Consistent lock order; keep tx short; SKIP LOCKED for queues. Table locks (DDL, VACUUM FULL) are the outage class.
