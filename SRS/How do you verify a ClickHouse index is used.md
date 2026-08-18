<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**EXPLAIN indexes = 1?**

EXPLAIN indexes = 1 shows which primary/skip/text indexes fired and Parts/Granules selected. If selected ≈ total, the WHERE does not match the ORDER BY prefix or skip index type. Also system.query_log (read_rows, marks). Don't trust 'we added an index' without this.
