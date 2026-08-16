<!--
reps: 0
priority: 0
-->
#Databases/ClickHouse #Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**How does the ClickHouse primary index work?**

Not unique, not per-row. Marks every granule by ORDER BY. WHERE on a prefix of the key binary-searches marks and skips other granules. Filter on a non-leading key → little/no skip. EXPLAIN indexes = 1: Parts/Granules selected vs total.
