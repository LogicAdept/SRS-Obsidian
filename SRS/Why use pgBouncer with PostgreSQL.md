<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**Why connection pooling? Session vs transaction mode?**

Each PG backend is a process (~few MB+). App spikes of connections exhaust max_connections/RAM. PgBouncer multiplexes. Transaction pooling: most SaaS; no session SET/LISTEN/prepared stmts across tx. Session pooling: keeps session state. Use transaction-scoped SET/advisory locks with transaction pooling. Don't just raise max_connections.
