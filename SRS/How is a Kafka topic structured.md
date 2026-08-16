<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Kafka: partition, offset, consumer group.**

Partition — шард топика. Offset — позиция в partition. Consumer group — каждый partition читает один consumer из группы.

**What is a topic vs a partition?**

Topic = named stream. Partition = ordered immutable log with monotonic offsets — unit of parallelism and ordering. Same key → same partition. Order is not global across partitions.
