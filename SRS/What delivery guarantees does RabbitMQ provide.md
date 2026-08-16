<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #API/Idempotency #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**At-most-once vs at-least-once in RabbitMQ?**

At-most-once: auto-ack or publish without confirms — may lose, no duplicates from the broker path. At-least-once: confirms + manual ack + redelivery on crash — no silent loss, duplicates possible. Exactly-once is not a broker primitive; you need idempotent consumers (unique event_id, upsert). Redelivery is normal.
