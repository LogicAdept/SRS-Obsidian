<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**What is transactional producer fencing?**

Each transactional.id has an epoch. A new producer with the same id increments the epoch; the broker fences the old instance (zombie after failover) so it cannot commit.
Needed so a restarted instance cannot complete a transaction the new instance already replaced.
