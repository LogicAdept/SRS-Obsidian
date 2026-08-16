<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**What is RabbitMQ?**

Open-source message broker (Erlang/OTP). Default protocol AMQP 0-9-1; also MQTT, STOMP, AMQP 1.0, HTTP plugins.
Producer publishes to an exchange; exchange routes via bindings to queues; consumer pulls/is pushed from a queue. Use for decoupling, async work, buffering spikes, task queues, RPC — not as a durable event log like Kafka.
