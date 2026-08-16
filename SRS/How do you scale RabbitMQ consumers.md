<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**How do you scale consumers?**

Add competing consumers on the same queue up to useful parallelism. Tune prefetch. Shard with multiple queues + consistent-hash or routing keys if one queue is the bottleneck. More nodes help connections/CPU; a classic queue is still one master. Quorum: leader still serializes that queue.
