<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**When is order guaranteed?**

Single queue + single consumer: FIFO for that queue. Multiple consumers, prefetch>1, requeue, or priority queues break strict order. Do not promise global order across queues. If order per key is required, one queue (or shard) per key and one consumer, or don't use RabbitMQ as a partitioned log (that's Kafka).
