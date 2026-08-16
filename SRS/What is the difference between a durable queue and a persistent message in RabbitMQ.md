<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**Durable queue vs persistent message?**

Durable queue/exchange: definition survives broker restart. Persistent message: delivery_mode=2, written toward disk. Need both (plus typically publisher confirms) for 'survive restart'. Transient messages on a durable queue still vanish. Persistent messages on a non-durable queue vanish when the queue is gone.
