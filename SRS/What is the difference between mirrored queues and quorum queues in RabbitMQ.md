<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**Mirrored classic vs quorum?**

Classic HA mirroring: policy ha-mode, master+mirrors, known split-brain/sync issues, deprecated. Quorum: Raft majority, predictable failover, recommended in 3.10+/4.x. Interview answer: new durable queues → quorum; mirroring only on legacy.
