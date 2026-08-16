<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**What do you do if a node dies?**

Clients reconnect to another node (or load balancer). Quorum queues elect a new leader if majority remains; minority cannot commit (Raft). Classic non-mirrored queue on the dead node is unavailable until the node returns. Don't use a 2-node quorum. After restart, check alarms, disk, replica catch-up.
