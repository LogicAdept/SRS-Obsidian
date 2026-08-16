<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**How do topic wildcards work?**

Routing key and binding key are dot-delimited. * = exactly one word. # = zero or more words. log.* matches log.info, not log.info.db. # matches everything. *.error matches app.error. Interview trap: * is not a regex '.'.
