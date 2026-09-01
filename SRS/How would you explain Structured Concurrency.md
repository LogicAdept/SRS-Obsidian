<!--
reps: 0
priority: 0
-->
#Java/Concurrency #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Structured Concurrency — что это?**

StructuredTaskScope (preview в Java 21): управление временем жизни задач. Все подзадачи привязаны к scope — при закрытии scope все незавершённые отменяются. ShutdownOnFailure: при первой ошибке все остальные отменяются. ShutdownOnSuccess: при первом успехе остальные отменяются. Замена разрозненным CompletableFuture.
