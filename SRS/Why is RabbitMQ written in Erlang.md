<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**Why is RabbitMQ written in Erlang?**

Erlang/OTP: lightweight processes, preemptive scheduling, clustering and failover primitives. The broker is an Erlang application; Erlang must be installed with the server. Interview trivia, but common.
