<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**Connection vs channel?**

Connection = TCP session (expensive: handshake, ~100KB+). Channel = lightweight multiplexed AMQP session on that TCP connection; publish/consume/declare happen on channels.
Long-lived connections, many channels. Do not share a channel across threads. Separate connections for publish vs consume so publisher flow-control does not stall consumer acks.
