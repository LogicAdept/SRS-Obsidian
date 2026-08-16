<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**What is rack awareness?**

broker.rack (and replica.selector) places replicas across racks/AZs so a single AZ outage does not take all replicas of a partition. Combined with RF=3 this is the usual multi-AZ story.
