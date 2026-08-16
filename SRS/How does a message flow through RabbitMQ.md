<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**Walk through RabbitMQ message flow.**

1) Producer opens connection+channel, publishes to an exchange with a routing key (and optional headers).
2) Exchange does not store messages; it routes by type + bindings.
3) Matching queues hold the message until a consumer acks (or auto-ack).
4) Consumer receives (push via basic.consume, or pull basic.get), processes, acks.
Unroutable: dropped, returned if mandatory, or sent to an alternate exchange.
