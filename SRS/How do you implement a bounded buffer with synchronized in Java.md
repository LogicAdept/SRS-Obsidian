<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronization #Career/Interview/Exercises #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Разница между synchronized-методом и synchronized-блоком.**

Метод захватывает this (для static — Class-объект). Блок — любой указанный объект. Блок обычно эффективнее.

**Чем synchronized(this) отличается от synchronized(privateLock)?**

this доступен извне — любой может случайно или намеренно synchronized(obj) на том же объекте. privateLock (private final Object lock = new Object()) — полный контроль, никто извне не может захватить.
