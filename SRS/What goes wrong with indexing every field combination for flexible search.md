<!--
reps: 0
priority: 0
-->
#Databases/Indexes #SystemDesign/Performance #SystemDesign/Tradeoffs #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**Why not index every search combo?**

Write amplification, bloat, planner confusion, unused indexes. Pick the 2–3 real access paths. For ad-hoc admin search: trigram/FTS or an external search index, not 2^n B-trees.
