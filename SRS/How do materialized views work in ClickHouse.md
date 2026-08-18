<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**Are CH MVs lazy?**

Eager INSERT triggers: each inserted block runs the MV SELECT into a target table (often Summing/AggregatingMergeTree). Not ON SELECT refresh. Failed MV can fail/block insert depending on settings. Refreshable MVs (scheduled snapshot) are a different feature (~24.8). Past data is not backfilled unless you INSERT SELECT.
