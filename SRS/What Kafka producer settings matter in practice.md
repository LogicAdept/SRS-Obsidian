<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**Which producer settings matter in interviews?**

bootstrap.servers, serializers, acks, retries/delivery.timeout.ms, enable.idempotence, linger.ms/batch.size, compression.type, max.in.flight.requests.per.connection. Tune acks + idempotence + in-flight together.
