<!--
reps: 0
priority: 0
-->
#Databases/ClickHouse #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**Why is ALTER UPDATE/DELETE expensive?**

Async rewrite of affected parts. One-row UPDATE can rewrite huge parts. Queue in Keeper; can stall replication. Prefer ReplacingMergeTree inserts, partition drop, lightweight delete where available. Interview: mutations ≠ InnoDB UPDATE.
