<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**What is an exchange?**

Routing entity. Producers never publish 'to a queue' in AMQP 0-9-1 — they publish to an exchange. The exchange uses type, routing key, headers, and bindings to choose zero or more queues (or other exchanges). Exchanges do not buffer the payload.
