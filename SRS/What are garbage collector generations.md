<!--
reps: 0
priority: 0
-->
#Java/JVM/GarbageCollector #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из шпаргалок Хабра (MishaBucha, 2025). Не сверен с официальной документацией. Не считать ответом для ревью.

**What are Young Generation and Old Generation?**

Источник: https://habr.com/ru/articles/967190/

Young Generation: Eden (новые объекты) и Survivor S0/S1. Old Generation — объекты, пережившие несколько minor GC в Young Gen.
