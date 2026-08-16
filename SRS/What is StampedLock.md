<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronization #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из шпаргалок Хабра (MishaBucha, 2025). Не сверен с официальной документацией. Не считать ответом для ревью.

**What is StampedLock?**

Источник: https://habr.com/ru/articles/966892/

Lock с write/read и ultra-fast optimistic read: ускоряет чтение и снижает contention.
