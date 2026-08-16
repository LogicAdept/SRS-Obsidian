<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**What is consumer ack?**

basic.ack tells the broker the message is done and can be dropped. Manual ack (auto_ack=false): crash before ack → redelivery to this or another consumer. auto_ack=true: broker forgets on delivery — faster, can lose work, prefetch does not bound in-flight. Production: manual ack after successful side effects (or after idempotent write).
