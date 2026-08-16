<!--
reps: 0
priority: 0
-->
#Java/Persistence/JPA #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Оптимистичная блокировка в JPA.**

Поле @Version (int/long/timestamp). При update Hibernate сравнивает версию — если не совпала, бросает OptimisticLockException.
