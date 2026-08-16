<!--
reps: 0
priority: 0
-->
#Java/JVM/GarbageCollector #Java/JVM/Tuning #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из шпаргалок Хабра (MishaBucha, 2025). Не сверен с официальной документацией. Не считать ответом для ревью.

**Which JVM flags matter for heap, stack, and GC logs?**

Источник: https://habr.com/ru/articles/967190/

-Xms / -Xmx — min/max heap. -Xss — размер стека на поток. -XX:+PrintGCDetails, -Xlog:gc — логи GC.
