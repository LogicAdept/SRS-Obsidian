<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #Messaging/Expiration #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**Delayed messages?**

1) Plugin x-delayed-message exchange: header x-delay milliseconds, then routes as direct/topic/fanout (x-delayed-type). Flexible per-message delay; plugin must be installed.
2) TTL + DLX: publish to a wait queue with message/queue TTL; on expiry the message dead-letters to the real queue. Per-message TTL only applies at queue head — mixed TTLs can stall. No plugin needed.
