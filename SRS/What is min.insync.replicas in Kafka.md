<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**What is min.insync.replicas?**

Topic/broker setting: how many replicas must ack a write when the producer uses acks=all.
Typical production: replication.factor=3, min.insync.replicas=2 — one broker can die without stopping writes, and you refuse writes rather than silently commit to a single replica.
Trap: acks=all + min.insync.replicas=1 still allows single-replica commits.
