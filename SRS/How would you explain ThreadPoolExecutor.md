<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Executors #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**ThreadPoolExecutor.**

corePoolSize, maxPoolSize, keepAliveTime, workQueue, threadFactory, rejectedExecutionHandler. newCachedThreadPool опасен — OOM.

**ThreadPoolExecutor — параметры.**

corePoolSize, maxPoolSize, keepAliveTime, workQueue (LinkedBlockingQueue/ArrayBlockingQueue/SynchronousQueue), threadFactory, rejectedExecutionHandler (AbortPolicy/CallerRunsPolicy/DiscardPolicy/DiscardOldestPolicy).
