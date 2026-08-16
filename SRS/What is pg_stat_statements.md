<!--
reps: 0
priority: 0
-->
#Databases/PostgreSQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**What is pg_stat_statements?**

Extension: aggregated query stats (calls, total/mean time, rows). First stop for 'what's slow'. Pair with EXPLAIN on the normalized query. pg_stat_activity: who is running now, idle in transaction (vacuum killer). Always-on in production interviews.

**Finding search queries that dominate time?**

Normalized SQL + total_exec_time. A 'simple' ILIKE on users may be top-1. Enable it. Pair with EXPLAIN on that query id.
