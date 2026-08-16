<!--
reps: 0
priority: 0
-->
#Databases/ClickHouse #SystemDesign/Performance #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**Why is SELECT ... FINAL slow?**

Merge-on-read for Replacing/Collapsing so you see collapsed rows now. Reads overlapping parts, merges in memory — CPU/RAM, not for hot dashboards. Prefer waiting for merges, argMax in the query, or an Aggregating MV. Distributed: FINAL is per-shard; keys must not split across shards.
