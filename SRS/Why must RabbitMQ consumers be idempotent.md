<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #API/Idempotency #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**Why idempotent consumers?**

Redelivery after crash, nack/requeue, network retry, publisher republish of unconfirmed messages. Processing twice must be safe (unique constraint, upsert, outbox id).
