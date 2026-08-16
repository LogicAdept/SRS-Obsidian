<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**What protocols does RabbitMQ support besides AMQP?**

AMQP 0-9-1 (core), AMQP 1.0 plugin, MQTT (3.1.1 plugin: QoS0/1, retained, LWT; QoS2 downgraded), STOMP, HTTP API. Interview: name AMQP first, then MQTT/STOMP for IoT/UI, not 'RabbitMQ is only AMQP'.
