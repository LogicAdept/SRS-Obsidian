<!--
reps: 0
priority: 0
-->
#Databases/PostgreSQL #Databases/SQL/Transactions #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**FOR UPDATE vs SKIP LOCKED vs NOWAIT?**

FOR UPDATE: lock rows, wait. NOWAIT: error if locked. SKIP LOCKED: skip locked rows — job queues, many workers. Pair with LIMIT. Still need a transaction. Classic interview for worker pools.
