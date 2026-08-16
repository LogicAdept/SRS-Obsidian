<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**What is a poison pill / poison message?**

A delivery that always fails (bad JSON, missing FK, bug). Requeue loops pin a consumer and grow unacked. Fix: delivery-limit, retry cap + DLQ, don't auto-ack, monitor redeliveries. Inspect DLQ; fix or drop.
