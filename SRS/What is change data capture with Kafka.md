<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**What is CDC with Kafka?**

Debezium (Connect source) streams DB changes (insert/update/delete) into Kafka. Avoids dual writes. Challenges: snapshot, schema evolution, per-key order, exactly-once to the sink (upsert by PK).
Use compacted topics for current-state tables; retain changelog topics for history if needed.
