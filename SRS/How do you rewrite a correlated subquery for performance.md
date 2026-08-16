<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**How do you replace a per-row subquery?**

JOIN (SELECT parent_id, MAX(ts) ... GROUP BY parent_id). Window: ROW_NUMBER() OVER (PARTITION BY parent ORDER BY ts DESC) FILTER rn=1. LATERAL (SELECT ... WHERE parent_id = p.id ORDER BY ts DESC LIMIT 1). Compare EXPLAIN; don't rewrite blindly if the planner already hashed it.
