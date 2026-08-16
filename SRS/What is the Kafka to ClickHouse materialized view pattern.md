<!--
reps: 0
priority: 0
-->
#Databases/ClickHouse #Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**Why MV TO MergeTree from Kafka?**

Engine table has no history; MV is the persistent sink. Transform JSONExtract* in the MV SELECT. At-least-once + Replacing for duplicates. Query the MergeTree, never the Kafka table. ClickPipes is the managed equivalent.
