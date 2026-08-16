<!--
reps: 0
priority: 0
-->
#Databases/PostgreSQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**What is LISTEN/NOTIFY?**

Lightweight pub/sub on a channel; payload after commit. Session-scoped — breaks under PgBouncer transaction pooling. Fine for cache invalidation on few connections, not a Kafka replacement.
