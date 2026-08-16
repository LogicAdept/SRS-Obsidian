<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**What is the default exchange?**

Pre-declared nameless direct exchange (""). Every queue is auto-bound with routing key = queue name, so publishing to "" with routing_key=my.queue looks like 'publish to queue'. You cannot bind/unbind the default exchange yourself. Still an exchange under the hood.
