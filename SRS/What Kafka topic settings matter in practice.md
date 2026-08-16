<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**Which topic settings matter?**

replication.factor, min.insync.replicas, retention.ms/bytes, cleanup.policy=delete|compact, segment.bytes, unclean.leader.election.enable=false, max.message.bytes.
