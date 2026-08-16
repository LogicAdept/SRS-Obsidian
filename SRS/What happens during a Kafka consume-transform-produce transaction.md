<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**Walk through a consume-transform-produce transaction.**

Producer initTransactions(). Consumer polls. beginTransaction(). Process and produce outputs. sendOffsetsToTransaction for consumed offsets. commitTransaction() — all visible or none. On failure abortTransaction().
read_committed consumers never see partial output. transactional.id must be unique per producer instance so a restarted instance fences the old one.
