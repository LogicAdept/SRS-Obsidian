<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #Java/Spring/AMQP #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**How does @RabbitListener work?**

Spring AMQP: ConnectionFactory, RabbitTemplate to publish, @RabbitListener on a method to consume. Container (Simple or Direct) pushes deliveries, acks on success, retries if configured. Queues/exchanges/bindings as beans or @RabbitListener bindings. Jackson MessageConverter for JSON. Manual ack via Channel if needed.
