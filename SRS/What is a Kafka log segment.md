<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**What is a log segment?**

A partition log is split into segment files (segment.bytes / segment.ms). Active segment is appended; older segments can be deleted (retention) or cleaned (compaction). Offset and time indexes sit beside each segment.
