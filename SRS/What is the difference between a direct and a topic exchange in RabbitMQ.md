<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**Direct vs topic exchange?**

Direct: binding key must equal routing key. Topic: routing key is dotted; bindings use * (one token) and # (zero or more). Use direct for exact destinations (order.created → order-queue). Use topic for hierarchical events (order.*.eu).
