<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**Which consumer settings matter?**

group.id, enable.auto.commit=false for at-least-once, max.poll.records, max.poll.interval.ms, session.timeout.ms, heartbeat.interval.ms, isolation.level, fetch.min.bytes / fetch.max.wait.ms.
