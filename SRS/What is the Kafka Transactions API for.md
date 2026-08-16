<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**What is the Kafka Transactions API for?**

1) Idempotent producer (enable.idempotence=true, default since Kafka 3.0): PID + sequence numbers, broker drops retry duplicates per partition.
2) Transactions: initTransactions, beginTransaction, produce, sendOffsetsToTransaction, commitTransaction. Unique transactional.id fences zombie producers.
3) Consumers: isolation.level=read_committed so aborted batches are hidden.
4) Kafka Streams: processing.guarantee=exactly_once_v2 packages this.
Idempotence alone is not end-to-end EOS across partitions or external systems.
