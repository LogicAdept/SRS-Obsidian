<!--
reps: 0
priority: 0
-->
#Databases/ClickHouse #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**When do you use ReplacingMergeTree?**

On merge, keep last row per ORDER BY (optional version column). CDC/upsert pattern. Dedup is async — queries can see duplicates until merge. FINAL forces merge-on-read (slow). Don't treat it as a unique constraint. Sharding key should keep the same ORDER BY on one shard if you need collapse.
