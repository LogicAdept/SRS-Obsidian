<!--
reps: 0
priority: 0
-->
#Java/Persistence/Hibernate #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Что такое LazyInitializationException и как с ним жить?**

Попытка обратиться к lazy-полю после закрытия сессии. Решения: JOIN FETCH в запросе, @EntityGraph, DTO-проекции, OpenSessionInView (анти-паттерн в проде).

**Что такое LazyInitializationException?**

Возникает, когда обращаешься к LAZY-полю после закрытия сессии Hibernate. Сценарий: достал Entity в @Transactional-методе, вернул наружу. Транзакция закрылась — сессия закрылась. В контроллере / сериализаторе обращаешься к LAZY-полю — БАХ. Решения: (1) @EntityGraph на репозиторий — указать, что грузить eager. (2) JOIN FETCH в JPQL. (3) DTO-проекция в сервисе. (4) Open Session In View — но это плохая практика.
