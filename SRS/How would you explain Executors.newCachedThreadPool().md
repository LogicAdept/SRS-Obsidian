<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Executors #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Чем опасен Executors.newCachedThreadPool() в проде?**

Неограниченное количество потоков — при всплеске нагрузки может положить JVM через OutOfMemoryError (unable to create new native thread).
