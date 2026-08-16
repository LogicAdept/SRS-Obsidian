<!--
reps: 0
priority: 0
-->
#Messaging/Broker #Patterns/Enterprise/Integration/Messaging #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**RabbitMQ as a message broker?**

RabbitMQ is a concrete broker: clients speak AMQP to exchanges/queues instead of point-to-point sockets. Adds routing, buffering, ack, vhosts.
