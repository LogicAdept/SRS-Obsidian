<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**Why does Kafka use pull (fetch) instead of push?**

Consumers fetch at their own rate — natural backpressure, no broker tracking per-consumer delivery. Slow consumers do not force the broker to buffer per client the way a push queue might.
Retention lets others catch up later. Contrast RabbitMQ push to consumers with per-message ack.
