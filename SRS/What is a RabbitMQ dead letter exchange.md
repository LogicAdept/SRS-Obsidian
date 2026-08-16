<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**What is DLX / DLQ?**

Queue argument x-dead-letter-exchange (optional x-dead-letter-routing-key). Messages go there when: nack/reject with requeue=false, TTL expires, queue max-length overflow, or quorum x-delivery-limit exceeded. DLX is a normal exchange; bind a DLQ to inspect/retry. Without DLX, rejected messages are dropped.
