<!--
reps: 0
priority: 0
-->
#Java/Streams #Java/Parallelism #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Parallel streams: в чём опасность?**

Все parallel streams делят общий ForkJoinPool.commonPool(). Если один параллельный стрим заблокировался на I/O — остальные ждут. Решение: кастомный ForkJoinPool: new ForkJoinPool(4).submit(() -> stream.parallel()...). Не использовать для I/O-bound задач.
