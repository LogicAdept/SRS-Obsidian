<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Messages #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**Competing consumers on RabbitMQ?**

N consumers on one queue; each delivery goes to one worker. Prefetch balances in-flight work. Scale-out workers. Not pub/sub — for copies use fanout and a queue per subscriber.
