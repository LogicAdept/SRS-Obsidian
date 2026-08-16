<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**What is a vhost?**

Namespace: isolated exchanges, queues, bindings, users/permissions. Default is /. Use vhosts to split prod/staging or tenants on one broker instead of separate clusters. Connection always targets a vhost.
