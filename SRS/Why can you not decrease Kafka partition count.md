<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**Why can you not decrease the number of partitions?**

Offsets and ordering are per partition. Merging partitions would scramble offset sequences and break committed consumer positions. Kafka only supports increasing partition count; shrinking means new topic + migrate.
