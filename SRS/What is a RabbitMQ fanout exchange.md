<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**What is a fanout exchange?**

Broadcast: every bound queue gets a copy. Routing key ignored. Classic pub/sub (email + SMS + audit from one event). Each subscriber should have its own queue bound to the same fanout — not share one queue if they all need the copy.
