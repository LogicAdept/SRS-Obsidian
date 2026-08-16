<!--
reps: 0
priority: 0
-->
#Java/JVM/GarbageCollector #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из шпаргалок Хабра (MishaBucha, 2025). Не сверен с официальной документацией. Не считать ответом для ревью.

**What is the default GC by Java version?**

Источник: https://habr.com/ru/articles/967190/

Java 8 — Parallel GC. Java 9+ — G1 GC. Некоторые JDK (например Azul Zulu) могут ставить ZGC или Shenandoah по умолчанию при latency-целях.
