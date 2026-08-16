<!--
reps: 0
priority: 0
-->
#Java/JVM/GarbageCollector #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из шпаргалок Хабра (MishaBucha, 2025). Не сверен с официальной документацией. Не считать ответом для ревью.

**What is ZGC?**

Источник: https://habr.com/ru/articles/967190/

Heap до терабайт. Паузы менее 10 мс независимо от размера heap. Почти все фазы concurrent. Для latency-чувствительных систем. Флаг: -XX:+UseZGC.
