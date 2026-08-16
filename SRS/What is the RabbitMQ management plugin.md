<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**What is the management UI / default ports?**

Plugin: HTTP API + UI. Default UI 15672 (user guest local-only). AMQP 5672, AMQPS 5671. rabbitmqadmin / rabbitmqctl for automation. UI shows queues, unacked, connections, channels — first stop when 'messages stuck'.
