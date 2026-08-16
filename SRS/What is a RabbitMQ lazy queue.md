<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**What is a lazy queue?**

Classic-queue mode: keep messages on disk early, small in-memory buffer. For huge backlogs so RAM does not explode. Throughput cost. Quorum already persists via Raft log — lazy is a classic-queue concept. Interview lists still ask it.
