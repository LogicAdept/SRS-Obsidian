<!--
reps: 0
priority: 0
-->
#Java/JVM/GarbageCollector #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из шпаргалок Хабра (MishaBucha, 2025). Не сверен с официальной документацией. Не считать ответом для ревью.

**What is G1 GC (Garbage First)?**

Источник: https://habr.com/ru/articles/967190/

Делит heap на регионы; регион может быть Young или Old. Этапы: Initial Mark, Concurrent Mark, Remark, Cleanup, Copy. Собирает сначала самые «мусорные» регионы. Старается не превышать MaxGCPauseMillis. Инкрементальная concurrent компактизирующая сборка Old Gen. Флаг: -XX:+UseG1GC. По умолчанию с Java 9+.
