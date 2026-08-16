<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**What is mandatory publish?**

If the exchange cannot route to any queue: mandatory=false (default) → drop or alternate exchange. mandatory=true → basic.return to the publisher. Pair with a return listener. Confirms tell you the broker accepted; mandatory tells you it was routable.
