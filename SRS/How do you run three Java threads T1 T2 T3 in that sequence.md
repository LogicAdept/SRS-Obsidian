<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Threads #Career/Interview/Exercises #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Virtual Threads (Java 21): pinning problem.**

Virtual Thread на synchronized блоке → pinning (привязка к platform thread, теряется лёгкость). Причина: synchronized работает через монитор объекта, JVM не может «припарковать» виртуальный поток. Решение: ReentrantLock вместо synchronized. Virtual Threads идеальны для I/O-bound, НЕ для CPU-bound (нет preemption).

**Virtual Threads (Java 21).**

Лёгкие потоки, управляемые JVM (не ОС). Thread.ofVirtual().start(). Миллионы потоков без проблем. НЕ подходят для CPU-bound задач (нет preemption). Идеальны для I/O-bound (сетевые запросы, БД). Executors.newVirtualThreadPerTaskExecutor().
