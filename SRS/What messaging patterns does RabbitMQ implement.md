<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**Which messaging patterns?**

Point-to-point / competing consumers (work queue). Pub/sub (fanout or topic + queue per subscriber). Request-reply/RPC. Routing (direct/topic). Dead-letter. Delayed/retry. Not a Kafka-style durable multi-subscriber log unless you use streams.
