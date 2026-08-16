<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**What is a routing key?**

Message metadata used by direct and topic exchanges. Direct: exact match to the binding key. Topic: dot-separated words, binding may use * and #. Fanout ignores it. Headers exchange ignores it and uses headers.
