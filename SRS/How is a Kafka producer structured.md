<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**Producer internals?**

Serialize key/value → partitioner → accumulate in a per-partition batch (linger.ms/batch.size) → send to partition leader → leader appends, followers replicate → ack per acks → retries on failure (idempotence prevents dupes).
