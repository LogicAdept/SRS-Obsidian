<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**What are RabbitMQ streams?**

Append-only, replicated log (not competing-consumer delete-on-ack). Many consumers read independently with offsets. High throughput via the stream protocol. Pick streams for fan-out history/replay; pick quorum queues for 'do this job once'.
