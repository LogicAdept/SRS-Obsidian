<!--
reps: 0
priority: 0
-->
#Java/Concurrency #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**CountDownLatch vs CyclicBarrier vs Semaphore.**

CountDownLatch: одноразовый счётчик, потоки ждут обнуления. CyclicBarrier: переиспользуемый, все потоки ждут друг друга. Semaphore: ограничение числа одновременных потоков (пул ресурсов).

**How does CyclicBarrier differ from CountDownLatch?**

Источник: https://habr.com/ru/articles/966892/

CyclicBarrier можно использовать повторно. Потоки ждут друг друга на await() (барьер), затем можно снова. CountDownLatch — одноразовый счётчик вниз.
