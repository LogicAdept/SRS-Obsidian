<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**What are under-replicated partitions (URP)?**

A partition whose ISR is smaller than the configured replication factor. Replication lag, slow disk, or network. URP > 0 sustained is a durability incident, not a yellow metric. Pair with ISR shrink alerts.
