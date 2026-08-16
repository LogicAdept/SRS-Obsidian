<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**Cluster vs federation vs shovel?**

Cluster: one logical broker, shared metadata, LAN, same version.
Federation: plugin, brokers stay independent; federated exchange replays/copies upstream publishes; federated queue moves messages only when local consumers need them (load sharing).
Shovel: configured consumer that unconditionally moves from source queue to dest exchange/queue (migration, DC link, more control). Can combine: clusters linked by federation/shovel.
