<!--
reps: 0
priority: 0
-->
#Messaging #DistributedSystems #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**Where does RabbitMQ sit as a broker?**

Broker in the middle: producers don't call consumers. RabbitMQ is a queue-oriented AMQP broker (routing + ack + HA queues). Contrast with Kafka (log) and with HTTP (sync). Same idea as the Message Broker EIP.
