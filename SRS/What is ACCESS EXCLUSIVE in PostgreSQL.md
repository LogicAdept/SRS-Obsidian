<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/SQL/Transactions #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**What does ACCESS EXCLUSIVE block?**

Strongest table lock: conflicts with everything including ACCESS SHARE (plain SELECT). Taken by DROP TABLE, TRUNCATE, VACUUM FULL, many ALTER TABLE rewrites, some index builds. That's why CONCURRENTLY and NOT VALID exist. Check pg_locks / wait_event Lock.
