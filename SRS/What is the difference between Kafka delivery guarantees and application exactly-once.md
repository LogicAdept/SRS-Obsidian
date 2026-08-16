<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #API/Idempotency #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**Why is broker exactly-once not enough for a database sink?**

Kafka EOS covers produce + offset commit inside Kafka. Writing to Postgres/HTTP is outside that atomic boundary. Crash after DB write before offset commit → duplicate side effect.
Need idempotent sink: unique event_id, upsert, or outbox/inbox table. This is the follow-up after someone recites transactions.
