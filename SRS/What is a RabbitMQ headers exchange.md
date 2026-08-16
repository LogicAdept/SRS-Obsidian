<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**What is a headers exchange?**

Routes by message header table, not routing key. x-match=all (AND) or any (OR). Heavier than direct/topic; use when routing depends on several attributes (format, tenant, version).
