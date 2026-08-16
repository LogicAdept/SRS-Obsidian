<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #Messaging/RequestReply #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**How do you implement request-reply / RPC?**

Client publishes request with reply_to (often exclusive callback queue) and correlation_id. Server consumes, processes, publishes response to reply_to with same correlation_id. Client matches ids. Timeouts, exclusive reply queues, don't block HTTP threads unbounded. Direct reply-to is a RabbitMQ optimization (pseudo-queue amq.rabbitmq.reply-to).
