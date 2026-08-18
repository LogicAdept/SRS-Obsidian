<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/Partitioning #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**How do you expire data?**

TTL DateTime + INTERVAL: drop rows/columns or move to cold volume. Partition TTL + DROP PARTITION is cheapest. Without TTL event tables grow forever. Moves/deletes still work through merges — not instant per row.
