<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**What is the Buffer engine?**

In-memory buffer that flushes to a destination MergeTree by size/time/rows. Smooths tiny inserts. Data can be lost on crash before flush. Alternative/complement to async_insert. Queries must hit Buffer+dest or you miss fresh rows.
