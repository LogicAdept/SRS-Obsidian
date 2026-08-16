<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**Federation vs shovel?**

Shovel: explicit endpoints, usually one-way, moves messages unconditionally, good for migration/aggregation.
Federation: policies + upstreams; exchange federation copies a stream; queue federation moves on demand if upstream has no local consumers. Better for geo topologies and upgrades without stretching a cluster.
