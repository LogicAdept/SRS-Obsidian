<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**What is bloat and how do you fix it?**

Dead tuples / sparse pages left by MVCC churn. Causes: heavy UPDATE/DELETE, long-running tx blocking vacuum, autovacuum too weak. Tune autovacuum_vacuum_scale_factor / thresholds; avoid idle-in-transaction; pg_repack for online rewrite. VACUUM FULL returns space to OS but takes ACCESS EXCLUSIVE — not a prod reflex.
