<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**What is an alternate exchange?**

If the target exchange has no matching binding, it can delegate to another exchange (AE) instead of dropping. Useful for capturing unroutable messages during topology changes. Different from DLX (DLX is queue-level after reject/TTL/overflow).
