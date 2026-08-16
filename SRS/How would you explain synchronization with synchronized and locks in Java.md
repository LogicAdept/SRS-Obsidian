<!--
reps: 0
priority: 0
-->
#Java/Concurrency #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из шпаргалок Хабра (MishaBucha, 2025). Не сверен с официальной документацией. Не считать ответом для ревью.

**Which lock types does the article list?**

Источник: https://habr.com/ru/articles/966892/

synchronized — один поток в блоке/методе. ReentrantLock — таймауты, interruptible lock. ReadWriteLock — много читателей, один писатель. StampedLock — write/read и optimistic read, меньше contention.
