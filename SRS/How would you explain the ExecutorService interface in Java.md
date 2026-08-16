<!--
reps: 0
priority: 0
-->
#Java/Concurrency #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из шпаргалок Хабра (MishaBucha, 2025). Не сверен с официальной документацией. Не считать ответом для ревью.

**What are Executor and ExecutorService?**

Источник: https://habr.com/ru/articles/966892/

Executor выполняет задачу (не обязательно асинхронно; может в вызывающем потоке). RejectedExecutionException, если не принял.
ExecutorService — очередь и планирование на пуле: Executors.newFixedThreadPool(10); submit(() -> ...).
