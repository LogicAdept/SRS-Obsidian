<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**What is a queue?**

Named buffer. Competing consumers on one queue: each message goes to one consumer. Survives restart only if durable; messages survive only if persistent (and typically with publisher confirms). Types: classic, quorum (Raft, recommended HA), stream (append-only log).
