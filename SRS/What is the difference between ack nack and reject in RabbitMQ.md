<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**ack vs nack vs reject?**

ack — success, remove. reject — fail one message; requeue=true puts it back, false dead-letters or drops. nack (RabbitMQ extension) — like reject but can nack a range (multiple=true). Infinite nack+requeue with one consumer = poison loop; use delivery-limit or DLX.
