<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**What happens when a Kafka broker fails?**

Follower dies: ISR may shrink; leaders keep serving.
Leader dies: controller elects a new leader from ISR; clients refresh metadata; brief produce/fetch errors.
Too many brokers die: partitions with no ISR leader go offline.
Controller dies: KRaft quorum elects another controller. Use rack awareness so replicas are not all in one AZ.
