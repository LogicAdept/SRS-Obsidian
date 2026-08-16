<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**What happens if you add partitions to an existing topic?**

New partitions start empty. Default partitioner hash changes: a key that always went to P2 may now go to P5. Per-key order for new records vs old history can split across partitions.
You cannot shrink partitions without recreating the topic and migrating data.
