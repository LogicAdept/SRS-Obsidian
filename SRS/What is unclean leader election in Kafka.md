<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**What is unclean leader election?**

If the leader dies and no ISR member is available, unclean.leader.election.enable=true lets an out-of-sync replica become leader — availability over durability, data loss possible.
false (preferred for critical topics): wait for an ISR replica; partition stays offline until one catches up.
Interviewers want: I leave unclean election off for orders/payments.
