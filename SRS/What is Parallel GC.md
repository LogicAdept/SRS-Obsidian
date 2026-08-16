<!--
reps: 0
priority: 0
-->
#Java/JVM/GarbageCollector #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из шпаргалок Хабра (MishaBucha, 2025). Не сверен с официальной документацией. Не считать ответом для ревью.

**What is Parallel GC (Throughput Collector)?**

Источник: https://habr.com/ru/articles/967190/

Несколько потоков для Young и Old Gen. Цель — максимальная пропускная способность, не минимум пауз. Для серверных приложений без жёстких требований к latency. Флаг: -XX:+UseParallelGC. По умолчанию в Java 8.
