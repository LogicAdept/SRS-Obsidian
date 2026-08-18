<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**Why is idle in transaction dangerous?**

Oldest xmin horizon: VACUUM cannot remove dead tuples still visible to that snapshot → bloat, wraparound pressure, replication lag (slots). Keep transactions short; statement_timeout / idle_in_transaction_session_timeout. BEGIN then coffee is an outage.
