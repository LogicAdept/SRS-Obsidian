<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #Java/Spring/AMQP #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**SimpleMessageListenerContainer vs DirectMessageListenerContainer?**

Simple: thread pool, consumers are threads looping basic.consume; classic default. Direct: consumers invoked on AMQP client threads, generally lower overhead, different concurrency model. Boot: spring.rabbitmq.listener.type=simple|direct. Interview: know both exist and retry advice must be on the container you actually use.
