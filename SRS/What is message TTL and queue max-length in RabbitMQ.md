<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #Messaging/Expiration #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**TTL and max-length?**

x-message-ttl / per-message expiration: drop or dead-letter after time. x-max-length / x-max-length-bytes: overflow drop-head or dead-letter (x-overflow). Use to bound queues. Pair overflow/TTL with DLX so messages are not silently deleted.
