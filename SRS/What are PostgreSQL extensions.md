<!--
reps: 0
priority: 0
-->
#Databases/PostgreSQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**What are extensions? Name a few.**

CREATE EXTENSION: packaged C/SQL (pg_stat_statements, pgcrypto, uuid-ossp, btree_gin, pg_trgm, vector/pgvector, postgis). Superuser or allowed list on managed clouds. Interview: pg_trgm for fuzzy LIKE, pgvector for embeddings 2025–26.
