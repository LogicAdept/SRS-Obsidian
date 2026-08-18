<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**How does the planner pick a plan?**

Cost model from pg_statistic (ANALYZE): MCV, histograms, correlation. Cheapest estimated plan wins. Stale/skewed stats → seq scan or nested loop explosion. CREATE STATISTICS for correlated columns. Implicit casts hide indexes. random_page_cost too high on SSD.

**Cost model and search?**

Stats + random_page_cost. Wrong n_distinct on a search column → seq scan. ANALYZE after loading dictionaries/data. Expression indexes need matching query shape.
