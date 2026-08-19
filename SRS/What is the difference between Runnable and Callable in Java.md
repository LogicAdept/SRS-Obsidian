<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Executors #Java/Async #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Чем Runnable отличается от Callable?**

Runnable — run() возвращает void, не может бросать checked-исключения. Подходит для «просто запусти». Callable<V> — call() возвращает V, может бросать Exception. Используется через ExecutorService.submit() и Future<V>.

**How do Runnable and Callable differ?**

Источник: https://habr.com/ru/articles/966892/

Оба — задача для потоков. Runnable запускают через Thread или ExecutorService; Callable — только через ExecutorService (результат/исключение).
