<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**A topic has 6 partitions and 8 consumers in one group. What happens?**

At most 6 consumers are assigned a partition. Two stay idle. Parallelism in one group is capped by partition count.
A second group.id would independently read all 6 partitions again (fan-out).
