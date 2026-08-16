<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**Why is Kafka described as log-structured?**

Each partition is an append-only log of segments on disk. Sequential writes and sequential reads, OS page cache. Consumers address by offset, not random message IDs.
This is why Kafka saturates disks/NICs with modest CPU. Indexes (offset and timestamp) map offset → file position.
