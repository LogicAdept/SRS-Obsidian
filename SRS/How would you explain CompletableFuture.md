<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Executors #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**CompletableFuture.**

thenApply: T → R. thenCompose: T → CF<R> (flatMap). thenCombine: объединение двух CF. exceptionally: обработка ошибки. Async-варианты выполняются в ForkJoinPool.commonPool() или указанном Executor.

**CompletableFuture.**

thenApply (map), thenCompose (flatMap), thenCombine (join двух). exceptionally. Async-варианты в ForkJoinPool.

**What is CompletableFuture?**

Источник: https://habr.com/ru/articles/966892/

Расширение Future: явно завершать, цепочки, колбэки. thenApply — функция над результатом. thenCompose — разворачивает вложенный CF. allOf ждёт все, anyOf — первый. supplyAsync(..., executor) — свой пул.
