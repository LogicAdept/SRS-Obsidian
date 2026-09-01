<!--
reps: 0
priority: 0
-->
#Java/Persistence/JPA #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Разница между save(), persist(), merge(), update().**

persist — для новых (JPA стандарт, не возвращает id). save — Hibernate-specific, возвращает id. merge — копирует detached в managed. update — прикрепляет detached.
