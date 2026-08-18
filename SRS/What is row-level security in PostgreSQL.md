<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**What is RLS?**

Policies appended to every query so the DB enforces which rows a role sees/changes. Multi-tenant SaaS pattern. Bypass: table owner / BYPASSRLS / superuser. Policies + non-leakproof operators can disable index use. With poolers, set tenant via set_config(..., true) transaction-local.
