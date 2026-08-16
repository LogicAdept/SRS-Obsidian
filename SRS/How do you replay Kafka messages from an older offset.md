<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**How do you replay messages from 3 days ago?**

Retention must still hold that data (retention.ms). Stop the app or use a new group.id. Reset offsets: kafka-consumer-groups.sh --reset-offsets --to-datetime, or Consumer.seek / seekToBeginning.
Downstream must tolerate duplicates. Do not reset a live group that is still committing.
