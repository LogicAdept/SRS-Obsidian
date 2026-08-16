<!--
reps: 0
priority: 0
-->
#Java/JVM/GarbageCollector #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из шпаргалок Хабра (MishaBucha, 2025). Не сверен с официальной документацией. Не считать ответом для ревью.

**What is Shenandoah GC?**

Источник: https://habr.com/ru/articles/967190/

Похож на ZGC, акцент на короткие паузы. Concurrent compacting. OpenJDK. Флаг: -XX:+UseShenandoahGC.
