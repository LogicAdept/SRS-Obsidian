<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**Consumer poll loop?**

subscribe/assign → poll() fetches from leaders → process → commit offsets. Heartbeat thread keeps membership. Group coordinator assigns partitions. Lag is log-end minus position.
