<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**How does Kafka handle a slow consumer?**

Lag = log-end offset minus consumer offset, per partition. Growing lag means consumers cannot keep up.
Causes: slow handler (DB, GC), too few consumers, hot partition (skewed keys), rebalance storm, slow sink.
Tools: kafka-consumer-groups.sh --describe, Burrow, Prometheus/JMX.
Fix: scale consumers up to partition count, speed up processing, review partition key, DLT for poison pills. Distinguish transient restart lag vs sustained lag.
