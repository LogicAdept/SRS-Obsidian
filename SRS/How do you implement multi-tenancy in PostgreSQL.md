<!--
reps: 0
priority: 0
-->
#Databases/PostgreSQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**Schema-per-tenant vs row-level RLS?**

Schema per tenant: isolation, painful at thousands of tenants, migrations × N. Row-level tenant_id + RLS: scales, must never forget the predicate (RLS is the seatbelt). DB-per-tenant: ops hell. Pooler: set tenant as transaction-local GUC, not session leftovers.
