<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**Typical production queue declare?**

durable=true, arguments: x-queue-type=quorum, x-dead-letter-exchange=..., x-delivery-limit=N, optional x-max-length. Publisher: persistent + confirms. Consumer: manual ack, bounded prefetch. This is the 2026 interview 'happy path'.
