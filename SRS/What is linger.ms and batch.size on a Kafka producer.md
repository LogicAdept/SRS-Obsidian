<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**What are linger.ms and batch.size?**

Producer batches records per partition. linger.ms waits a few ms to fill a batch; batch.size is the max batch bytes.
Larger batches → higher throughput, higher latency. Tune after measuring, not from folklore. Combine with compression.type (lz4/zstd).
