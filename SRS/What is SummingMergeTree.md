<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**SummingMergeTree vs AggregatingMergeTree?**

Summing: sums numeric columns not in the sorting key during merge — counters. Aggregating: stores AggregateFunction states (sumState, uniqState) for arbitrary rollups. MV target is often one of these. Not for 'latest row' — that's Replacing.
