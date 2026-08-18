<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**Kafka engine plus materialized view?**

Kafka engine table is a consumer (not storage). MV TO MergeTree transforms and persists. Offsets commit after insert → at-least-once; duplicates possible → ReplacingMergeTree or idempotent keys. Batch via kafka_max_block_size. Don't INSERT one event at a time from the app if you can use this pipeline.
