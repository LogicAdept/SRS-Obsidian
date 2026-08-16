<!--
reps: 0
priority: 0
-->
#Databases #Java/JDBC #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**Pooling for Postgres processes?**

Process-per-connection is expensive. PgBouncer transaction mode in front. Don't explode max_connections.
