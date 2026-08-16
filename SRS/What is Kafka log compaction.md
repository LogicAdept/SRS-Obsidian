<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**What is log compaction versus time-based retention?**

delete (retention.ms / retention.bytes): drop old segments by age or size. Enables replay of history until expiry.
compact: keep the latest record per key; tombstone (null value) deletes a key after delete.retention.ms. Used for changelogs, compacted state, __consumer_offsets.
Compaction is not immediate — duplicates remain until the log cleaner runs. Compaction is not infinite raw history.
