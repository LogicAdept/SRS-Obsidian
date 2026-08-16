<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**How do you get durability in practice?**

Durable queue + persistent publish + publisher confirms + (for HA) quorum queue. Manual consumer acks. Even then a crash before fsync can lose a tiny window — quorum + confirms is the modern answer. Classic mirrored queues are deprecated.
