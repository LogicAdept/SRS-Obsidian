<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**What do you monitor?**

Queue depth (ready), unacked, publish vs ack rate, consumer count, memory/disk alarms, connection/channel count (leaks), quorum replica status, DLQ growth, redeliveries. Tools: Management UI (15672), rabbitmqctl list_queues, Prometheus plugin + Grafana. Build-up: slow/crash-loop consumers, prefetch 0, no consumers, poison loop.
