<!--
reps: 0
priority: 0
-->
#Databases/Indexes #SystemDesign/Performance #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**When Postgres seq-scans?**

Low selectivity, tiny table, stale stats, high random_page_cost. Bitmap Heap Scan is the middle ground.

**When is a seq scan the right plan?**

Low selectivity, tiny table, stale stats, random I/O of index+heap worse than sequential. Bitmap scan is the middle. Forcing an index can be slower.
