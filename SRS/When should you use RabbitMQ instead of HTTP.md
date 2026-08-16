<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**When is a broker better than a synchronous API?**

When the caller must not wait, work can be buffered, multiple independent consumers, retry/isolation from a down dependency, load leveling. Keep HTTP for request/response the user waits for. Don't put every CRUD through a queue.
