<!--
reps: 0
priority: 0
-->
#Java/Persistence/JPA #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Кэши Hibernate.**

First-level: автоматический, привязан к Session. Гарантирует identity (один PK = один объект). Second-level: опциональный, общий (EhCache, Caffeine, Infinispan). Query cache: кэширует JPQL-результаты. В банковских проектах: first-level всегда, second-level осторожно.

**Состояния сущности в Hibernate.**

Transient (новый объект, Hibernate не знает), Persistent/Managed (связан с сессией), Detached (был persistent, но сессия закрыта), Removed (помечен на удаление).

**Кэши Hibernate.**

First-level: привязан к Session, автоматический. Second-level: общий (EhCache, Caffeine), опциональный. Query cache: кэширует JPQL-результаты.
