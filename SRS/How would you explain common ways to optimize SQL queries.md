<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/Relational/MySQL #Databases/Relational/PostgreSQL #Databases/Relational/Oracle #SystemDesign/Performance #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**Postgres-specific SQL optimization?**

EXPLAIN (ANALYZE, BUFFERS), stats, partial/expression/covering indexes, avoid wrapping columns, work_mem spills, vacuum/bloat, partition prune. Rewrite correlated subqueries (LATERAL / window).

**Generic SQL optimization checklist?**

Sargable predicates, EXPLAIN ANALYZE, indexes for WHERE/JOIN/ORDER BY, covering, avoid SELECT *, rewrite correlated subqueries, UNION ALL, keyset pagination, stats, don't LIKE '%x%' on B-tree.
