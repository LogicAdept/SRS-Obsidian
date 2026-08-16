<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**Why can retries break ordering if max.in.flight.requests.per.connection > 1?**

Without idempotence, a failed batch may retry after a later batch already succeeded — records for the same partition can land out of order.
Idempotent producer (default in 3.0+) plus bounded in-flight requests preserves per-partition order while allowing retries.
