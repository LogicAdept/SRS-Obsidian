<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**What is a RabbitMQ cluster?**

Several Erlang nodes sharing users/vhosts/metadata. A client can connect to any node. Classic queue contents historically lived on one node unless mirrored. Clustering ≠ durability by itself. Cross-DC: prefer federation/shovel, not a stretched cluster. Erlang cookie and matching versions matter.
