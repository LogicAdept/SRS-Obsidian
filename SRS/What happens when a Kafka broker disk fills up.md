<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**What happens when a broker runs out of disk?**

The broker stops accepting writes for partitions on that disk. If it is a leader, producers get errors.
Prevent: retention.ms/bytes per topic, alerts at 70–80% disk, log.retention.check.interval.ms. Compacted topics need extra space during cleaning.
