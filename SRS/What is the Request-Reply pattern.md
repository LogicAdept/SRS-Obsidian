<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**Request-reply on RabbitMQ?**

reply_to + correlation_id, often exclusive callback queue or direct reply-to. Server publishes the response to reply_to. Timeouts required.
