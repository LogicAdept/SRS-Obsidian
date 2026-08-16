<!--
reps: 0
priority: 0
-->
#Java/Spring/Cloud/Stream #Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**Why Spring Cloud Stream instead of Spring AMQP?**

Binder abstraction: same functional/Supplier-Consumer code against Kafka or Rabbit via binder deps. Less broker-specific topology code. Trade-off: leaky abstraction, extra layer. Use raw Spring AMQP when you need AMQP topology control (DLX args, confirms, channels).
