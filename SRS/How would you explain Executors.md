<!--
reps: 0
priority: 0
-->
#Java/Language #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Виды пулов в Executors.**

newFixedThreadPool, newCachedThreadPool, newSingleThreadExecutor, newScheduledThreadPool. В проде часто создают ThreadPoolExecutor вручную, чтобы контролировать очередь и политику отказа.

**Виды пулов потоков в Executors.**

newFixedThreadPool, newCachedThreadPool, newSingleThreadExecutor, newScheduledThreadPool, newWorkStealingPool. Для прода обычно создают ThreadPoolExecutor вручную, чтобы контролировать очередь.
