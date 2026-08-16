<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**How do competing consumers share a queue?**

Several consumers on one queue: each message is delivered to only one (round-robin / next available, limited by prefetch). Scale workers = more consumers on the same queue. Pub/sub copies need fanout/topic + a queue per subscriber, not many consumers on one queue.
