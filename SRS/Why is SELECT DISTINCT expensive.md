<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**Why can DISTINCT hide a bad join?**

DISTINCT sorts or hashes the whole result to drop dupes — often a band-aid for join fan-out. Prefer unique join keys or GROUP BY of what you actually need. EXPLAIN: Unique / HashAggregate / Sort on a huge input.
