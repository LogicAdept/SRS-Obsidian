<!--
reps: 0
priority: 0
-->
#Java/OOP #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**ConcurrentHashMap: Java 7 vs Java 8.**

Java 7: массив Segment (ReentrantLock), каждый сегмент — свой HashMap. Java 8: убрали Segment, CAS + synchronized на головах бакетов (лучше параллелизм). Treeify при 8 коллизиях.
