<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**What is the difference between acks=0, acks=1, and acks=all?**

acks=0: fire-and-forget, no broker ack, fastest, may lose data.
acks=1: wait until the partition leader writes the record; loss if the leader dies before followers replicate.
acks=all (or -1): wait until all in-sync replicas (ISR) ack. Strongest durability, higher latency.

Interview trap: acks=all is only as strong as min.insync.replicas. Pair RF=3 with min.insync.replicas=2. Use acks=0 only for loss-tolerant metrics.
