<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**How do you retry without an infinite loop?**

Do not nack+requeue forever on a poison message.
Pattern: TTL wait-queue → DLX back to work queue, increment x-death / custom header, after N times send to parking DLQ.
Quorum: x-delivery-limit then DLX. Spring: RetryInterceptor + RejectAndDontRequeueRecoverer so exhausted retries dead-letter.
Optional: delayed-message exchange plugin for backoff without a stack of TTL queues.
