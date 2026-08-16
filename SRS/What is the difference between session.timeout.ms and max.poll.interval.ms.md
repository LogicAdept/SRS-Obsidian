<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**What is the difference between session.timeout.ms and max.poll.interval.ms?**

session.timeout.ms: if heartbeats stop, the member is dead and a rebalance starts. heartbeat.interval.ms should be ~1/3 of session timeout.
max.poll.interval.ms: max time between poll() calls. Long processing without poll kicks the consumer even if heartbeats still run.
Pattern: poll often; hand work to a pool; pause/resume for backpressure. Never run a 5-minute DB call on the listener thread.
