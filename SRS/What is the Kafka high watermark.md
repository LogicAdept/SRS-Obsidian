<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**What is the high watermark versus log end offset?**

LEO (log end offset): next offset the leader will append — includes data not yet replicated to the ISR.
High watermark (HW): last offset known to be replicated to the ISR; consumers typically only read up to HW so they do not see data that could be lost on leader failover.
