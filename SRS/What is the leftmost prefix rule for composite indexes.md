<!--
reps: 0
priority: 0
-->
#Databases/Indexes/Composite #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**Why does (a,b,c) not help WHERE b = ?**

B-tree is ordered by a, then b, then c. Equality/range on a prefix works: a; a+b; a+b+c. Skipping a (filter only b) generally cannot seek — unless skip-scan on low-cardinality leading cols (MySQL 8+; not the Postgres default story). Put equality columns before range; match real WHERE/ORDER BY.

**ORDER BY prefix in ClickHouse?**

Sparse index only skips when WHERE constrains a left prefix of ORDER BY. WHERE ts= without leading user_id (if ORDER BY user_id, ts) barely skips. Same verbal rule as B-tree, different structure (granules not rows).
