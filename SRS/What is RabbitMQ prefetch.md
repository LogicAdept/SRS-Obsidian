<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**What is prefetch (basic.qos)?**

Max unacked messages outstanding on a channel/consumer. Default unset/0 is unlimited — broker can dump the queue into the client, OOM, unfair vs other consumers. Set prefetch (tens for slow handlers, higher for tiny jobs). Prefer per-consumer (global=false). Quorum queues: prefetch still matters.
