<!--
reps: 0
priority: 0
-->
#Databases/ClickHouse #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**What is SAMPLE?**

SAMPLE 0.1 with a sample key (often in ORDER BY, e.g. intHash64(user_id)) reads a fraction of granules for approximate metrics. Need a declared SAMPLE BY. Not a substitute for a skip index on a search predicate.
