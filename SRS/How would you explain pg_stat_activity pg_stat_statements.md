<!--
reps: 0
priority: 0
-->
#Java/Language #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**pg_stat_activity и pg_stat_statements — что показывают?**

pg_stat_activity: текущие запросы, их состояние (active/idle/waiting), PID, query_start. Для поиска long-running queries и блокировок. pg_stat_statements: статистика по запросам (calls, total_time, mean_time, rows). Для поиска самых тяжёлых запросов. Нужен extension (CREATE EXTENSION pg_stat_statements).

**Activity vs statements?**

activity: live sessions, wait events, idle in transaction. statements: cumulative slow-query ranking.
