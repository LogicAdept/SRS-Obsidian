<!--
reps: 0
priority: 0
-->
#Java/Language #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Deadlock, livelock, starvation.**

Deadlock — два потока ждут друг друга. Livelock — активны, но не прогрессируют (оба уступают). Starvation — поток не получает CPU/ресурс.

**Deadlock, livelock, starvation — в чём разница?**

Deadlock: два потока ждут друг друга. Livelock: потоки активны, но не прогрессируют. Starvation: поток не получает ресурс.

**How do deadlock and livelock differ?**

Источник: https://habr.com/ru/articles/966892/

Deadlock: потоки навсегда ждут ресурсы друг друга, прогресса нет. Избегать: один порядок блокировок, tryLock(timeout), меньше вложенных lock.
Livelock: не заблокированы, но бесконечно уступают друг другу, прогресса тоже нет. Избегать: jitter/backoff, таймауты, пересмотреть кооперацию.
