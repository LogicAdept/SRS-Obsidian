<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/ConcurrentHashMap #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**ConcurrentHashMap Java 8.**

CAS + synchronized на головах бакетов. Treeify при 8 коллизиях. null запрещён. computeIfAbsent атомарен.

**What concurrent collections does the article mention?**

Источник: https://habr.com/ru/articles/966892/

java.util.concurrent без внешней синхронизации. ConcurrentHashMap — быстрые concurrent read/write, удобен как согласованный кэш. CopyOnWriteArrayList — копирует массив при модификации.
