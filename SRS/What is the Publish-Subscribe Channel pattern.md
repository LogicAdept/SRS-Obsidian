<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**Pub/sub in RabbitMQ?**

Fanout (or topic) exchange + one queue per subscriber. Each subscriber gets a copy. Sharing one queue among subscribers is competing consumers, not pub/sub.
