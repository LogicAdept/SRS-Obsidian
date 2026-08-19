<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Executors #Java/Parallelism #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из шпаргалок Хабра (MishaBucha, 2025). Не сверен с официальной документацией. Не считать ответом для ревью.

**What is ForkJoinPool?**

Источник: https://habr.com/ru/articles/966892/

Ядро fork/join (Java 7). Рекурсивные задачи без потока на каждую подзадачу: fork разделить, join дождаться. Work-stealing перераспределяет работу между потоками.
