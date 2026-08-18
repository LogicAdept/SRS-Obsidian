<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**ADD INDEX vs MATERIALIZE INDEX?**

ALTER ADD INDEX only affects new parts. MATERIALIZE INDEX rebuilds on old parts (mutation-like cost). Until then EXPLAIN shows no skip. Same for text indexes. Plan disk/CPU like a backfill.
