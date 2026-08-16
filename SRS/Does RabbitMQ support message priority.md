<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**Does RabbitMQ have priority queues?**

Classic queues: x-max-priority at declare; messages with higher priority delivered first; unset = 0. Extra CPU/memory. Quorum queues historically lack (or limit) priority — don't assume priority on quorum. Overuse is an interview smell.
