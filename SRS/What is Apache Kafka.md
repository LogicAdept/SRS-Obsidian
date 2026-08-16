<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**What is Apache Kafka versus a traditional queue?**

Distributed append-only partitioned log. Consumers pull and track offsets. Retention by time/size/compaction, replay, multiple independent consumer groups.
Unlike a classic queue, a record is not deleted when one consumer acks it.
