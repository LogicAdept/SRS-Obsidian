<!--
reps: 0
priority: 0
-->
#Java/Persistence/Hibernate #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Pessimistic vs optimistic locking.**

Pessimistic: SELECT ... FOR UPDATE блокирует строку. Optimistic: версия (@Version) — при commit проверяется, изменилась ли она.
