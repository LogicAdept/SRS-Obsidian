<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**What is FDW?**

SQL/MED: query remote data as foreign tables (postgres_fdw, file_fdw, S3-ish wrappers). Join local + remote; pushdown when possible. Not a silver shard. Use for archive/cold data or federated reads, not as a hidden microservice bus.
