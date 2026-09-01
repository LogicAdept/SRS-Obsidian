<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Executors #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Какие типы пулов есть в Executors?**

newFixedThreadPool(n) — фиксированный размер. newCachedThreadPool() — растёт по необходимости, потоки умирают через 60 сек простоя. newSingleThreadExecutor() — один поток. newScheduledThreadPool() — для отложенных и периодических задач.
