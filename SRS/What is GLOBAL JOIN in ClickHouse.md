<!--
reps: 0
priority: 0
-->
#Databases/ClickHouse #Databases/Replication #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**GLOBAL IN / JOIN?**

Coordinator runs the right subquery, broadcasts the small set to shards, local join. Use when the right side is small. Huge right side → memory blowup. Prefer dictionaries or co-located sharding. Ordinary JOIN on Distributed can surprise you with per-shard incomplete dims.
