<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**Why does a queue grow?**

Consumers slower than publishers, consumers down, unacked pile (prefetch too high / stuck handler), poison requeue, missing consumers, routing into one hot queue. Fix: scale consumers, speed handler, bound queue (max-length + DLX), prefetch, check unacked in UI.
