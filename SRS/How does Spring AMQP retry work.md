<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #Java/Spring/AMQP #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**How do you retry in Spring AMQP?**

Listener advice chain: RetryInterceptorBuilder (stateless/stateful), max attempts, backoff, recoverer. Default recoverer may log-and-discard; production: RejectAndDontRequeueRecoverer so the broker DLXs after retries. spring.rabbitmq.listener.simple.retry.enabled on Boot auto-config. Stateful retry if you need transactions rolled back between attempts. Blocking retry occupies the consumer thread — prefer TTL/DLX delay queues for long backoff.
