<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**Why separate publisher and consumer connections?**

Broker may apply flow control on a publishing connection when queues/replication cannot keep up. Acks from consumers on the same TCP connection can stall. Pattern: at least one connection to publish, one to consume per process.
