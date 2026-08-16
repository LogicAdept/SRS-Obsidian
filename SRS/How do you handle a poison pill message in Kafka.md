<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**How do you handle a poison message that fails forever?**

A poison pill blocks a partition if you retry forever on the same offset.
Pattern: limited retries with backoff, then Dead Letter Topic (Spring DefaultErrorHandler / DeadLetterPublishingRecoverer) with key, partition, offset, exception. Alert on DLT rate. Manual triage. Do not skip silently on money paths.
