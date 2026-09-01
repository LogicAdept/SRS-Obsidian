<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Executors #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**CompletableFuture: thenApply vs thenCompose vs thenCombine.**

thenApply — преобразование результата. thenCompose — flatMap для CompletableFuture (нужен, когда лямбда возвращает CompletableFuture). thenCombine — объединение двух.

**CompletableFuture: thenApply vs thenCompose vs thenCombine.**

thenApply: преобразование результата. thenCompose: flatMap для CompletableFuture. thenCombine: объединение двух результатов.
