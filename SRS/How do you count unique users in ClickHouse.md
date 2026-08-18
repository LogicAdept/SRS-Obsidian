<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/SQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**uniq vs uniqExact?**

uniq()/uniqCombined: HyperLogLog-style approximate, cheap. uniqExact: exact, heavy. AggregatingMergeTree + uniqState for rollups. Don't COUNT DISTINCT on raw 1e11 events in the dashboard path — pre-aggregate.
