<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**What are the main exchange types?**

Direct — exact routing-key match (can fan-out to several queues with the same key).
Fanout — broadcast to all bound queues; routing key ignored (pub/sub).
Topic — pattern match: * one word, # zero or more words (e.g. log.* matches log.info).
Headers — match message headers (all/any); for complex criteria without a routing key.
Also: default exchange (nameless direct), delayed-message plugin, consistent-hash (plugin).
