<!--
reps: 0
priority: 0
-->
#Databases/ClickHouse #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**async_insert vs client batching?**

Server buffers small inserts into larger parts (flush by time/size). Use when 1000s of clients cannot batch. Tradeoff: durability until flush (wait_for_async_insert). Not a substitute for Kafka MV batching. Stops part storms from sync one-row writes.
