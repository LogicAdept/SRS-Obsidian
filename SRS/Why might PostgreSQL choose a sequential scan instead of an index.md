<!--
reps: 0
priority: 0
-->
#Databases/PostgreSQL #Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**Why seq scan over an index?**

Small table, low selectivity (most rows match), random_page_cost high vs seq (HDD defaults; lower on SSD), stale stats (ANALYZE), wrong index type, function on column hides index, RLS + non-leakproof ops. EXPLAIN (ANALYZE, BUFFERS): estimate vs actual rows mismatch → stats.

**Seq scan despite an index (search queries)?**

Selectivity, stats, function/cast, LIKE '%x%', random_page_cost. Trigram/FTS indexes are a different access method — a B-tree on the column will not help contains-search.
