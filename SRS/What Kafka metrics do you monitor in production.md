<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**What metrics do you monitor in production Kafka?**

Consumer lag vs SLO. Under-replicated / offline partitions. ISR shrink. Produce/fetch latency. Disk usage. Request error rates. Alert on sustained URP and lag growth, not only process-up.
