<!--
reps: 0
priority: 0
-->
#Java/Persistence/JPA #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**JOOQ vs Hibernate.**

JOOQ: типизированный SQL, compile-time проверка запросов, нет dirty checking. Hibernate: ORM, lazy loading, кэширование. В Путешествиях используют оба — JOOQ для сложных запросов, Hibernate для CRUD.
