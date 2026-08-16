<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**How does RabbitMQ implement a dead letter channel?**

Queue x-dead-letter-exchange (+ optional routing key) → DLX → DLQ. Triggers: reject/nack requeue=false, TTL, max-length, quorum delivery-limit. Inspect, retry with delay, or park. Without DLX, rejected messages vanish.
