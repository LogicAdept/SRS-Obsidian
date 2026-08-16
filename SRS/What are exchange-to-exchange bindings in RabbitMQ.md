<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**Can you bind exchanges to exchanges?**

Yes (AMQP extension). An exchange can route to another exchange, composing topologies (fanout of topics). Useful for sharing a stream of events across routing layers without extra queues.
