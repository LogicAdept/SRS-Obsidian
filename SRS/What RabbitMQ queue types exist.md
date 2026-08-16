<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**Classic vs quorum vs stream?**

Classic — original, good for transient/exclusive, priorities, some TTL tricks; not for HA.
Quorum — Raft replicated, default for durable competing-consumer work.
Stream — append-only log, multiple independent consumers, offset/time replay, high throughput (Stream protocol). Closer to Kafka than to a work queue.
