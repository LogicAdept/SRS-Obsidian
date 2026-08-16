<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**12 partitions, 4 consumers; one consumer dies. What happens?**

Each of 4 had 3 partitions. Rebalance: 3 remaining split 12 (e.g. 4/4/4). Consumption pauses during rebalance (less with cooperative sticky). session.timeout.ms controls how fast death is detected.
