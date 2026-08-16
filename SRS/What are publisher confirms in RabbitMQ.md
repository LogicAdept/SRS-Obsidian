<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**What are publisher confirms?**

Channel mode (confirm.select): broker async-acks/nacks publishes once the message is accepted (for quorum: after majority WAL). Without confirms basic.publish is fire-and-forget — crash/network can lose the message. Prefer confirms over AMQP transactions (faster). Unconfirmed after timeout → treat as unknown, republish if idempotent. mandatory=true returns unroutable messages to the publisher.
