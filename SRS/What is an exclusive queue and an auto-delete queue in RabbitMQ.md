<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**Exclusive vs auto-delete?**

Exclusive: only the declaring connection may use it; deleted when that connection closes (typical RPC reply queue). auto-delete: deleted when the last consumer unsubscribes. Durable exclusive is still tied to the connection. Don't use exclusive for shared work queues.
