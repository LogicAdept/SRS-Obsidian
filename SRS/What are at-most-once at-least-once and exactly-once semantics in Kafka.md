<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #API/Idempotency #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**Explain at-most-once, at-least-once, and exactly-once in Kafka.**

At-most-once: commit offset before processing (or acks=0). May lose records, no duplicates.
At-least-once: process then commit; retries on. No loss, duplicates possible. Default production pattern plus idempotent handlers.
Exactly-once: idempotent producer + transactions (and isolation.level=read_committed on consumers), or Kafka Streams exactly_once_v2.
EOS does not magically dedupe your database — sinks still need upserts or unique event_id.

**What delivery guarantees does the Habr cheat-sheet list?**

Источник: https://habr.com/ru/articles/968844/

At-most-once: 0 или 1 раз, возможна потеря, без дублей. At-least-once: ≥1, возможны дубли. Exactly-once: по статье Kafka сама по себе полноценный EOS не даёт — нужен доп. механизм, например Outbox + таблица обработанных ID. (Это упрощение шпаргалки, не сверка с Kafka transactions.)
