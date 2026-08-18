<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**What are advisory locks?**

App-level locks on bigint keys, not row locks. Session: pg_advisory_lock until unlock/disconnect. Transaction: pg_advisory_xact_lock — safer with PgBouncer transaction pooling. Use for 'only one cron'. Don't confuse with FOR UPDATE.
