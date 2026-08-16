<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #Messaging #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**Same group vs different group?**

Same group.id: they split partitions, each record processed once per group. Different group.id: both read the full topic independently (pub/sub fan-out).
