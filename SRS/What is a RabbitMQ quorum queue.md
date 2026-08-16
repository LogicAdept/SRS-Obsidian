<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**What is a quorum queue?**

Replicated queue (RabbitMQ 3.8+, default recommendation for durable work). Raft: leader + followers, confirm after majority WAL. Declare x-queue-type=quorum. Use publisher confirms + manual acks. Poison: x-delivery-limit. Trade-offs vs classic: no (or limited) priority/some TTL features; higher disk. Never new classic mirrored queues.
