<!--
reps: 0
priority: 0
-->
#Java/Language #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Каскадные операции: что делает CascadeType.ALL?**

PERSIST + MERGE + REMOVE + REFRESH + DETACH. Опасность: CascadeType.REMOVE при OneToMany — удаление родителя удалит ВСЕХ детей. Если детей 10 000 — 10 000 DELETE запросов. orphanRemoval=true — удаляет «осиротевших» детей при удалении из коллекции.
