<!--
reps: 0
priority: 0
-->
#Java/Persistence/Hibernate #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**LazyInitializationException.**

Обращение к lazy-полю после закрытия сессии. Решения (от лучшего к худшему): DTO-проекция (SELECT NEW), JOIN FETCH (@Query), @EntityGraph(attributePaths), @BatchSize(size=100). НЕ решение: OpenSessionInView (анти-паттерн — создаёт N+1 в представлении).

**LazyInitializationException.**

Обращение к lazy-полю после закрытия сессии. Решения: JOIN FETCH, @EntityGraph, DTO. OpenSessionInView — анти-паттерн.

**LIE vs OSIV vs N+1?**

Lazy association accessed with no Session (after @Transactional ended, or OSIV off). Fix: fetch in the transaction (JOIN FETCH/graph), DTO mapping, not EAGER everywhere. OSIV hides it and causes N+1 during JSON serialize.
