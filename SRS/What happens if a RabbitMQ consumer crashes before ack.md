<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**Consumer crash before ack?**

With manual ack the message is unacked; when the channel/connection dies the broker requeues and redelivers (possibly to another consumer). redelivered flag may be set. This is why handlers must be idempotent. auto_ack: message is already gone — lost.
