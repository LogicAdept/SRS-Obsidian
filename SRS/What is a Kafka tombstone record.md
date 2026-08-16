<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**What is a tombstone in Kafka?**

A record with a key and a null value. On a compacted topic the log cleaner eventually removes previous values for that key and then the tombstone itself after delete.retention.ms.
Used to delete an entity from a compacted changelog (user gone, config removed).
