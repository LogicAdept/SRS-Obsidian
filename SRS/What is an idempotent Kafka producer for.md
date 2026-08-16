<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #API/Idempotency #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**What is an idempotent producer?**

1) Idempotent producer (enable.idempotence=true, default since Kafka 3.0): PID + sequence numbers, broker drops retry duplicates per partition.

**What is idempotence in Kafka according to the article?**

Источник: https://habr.com/ru/articles/968844/

Идемпотентность — гарантия, что сообщения не будут обработаны более одного раза; важна для надёжной передачи между producer и consumer.
