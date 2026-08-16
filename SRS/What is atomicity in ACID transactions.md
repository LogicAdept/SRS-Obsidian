<!--
reps: 0
priority: 0
-->
#Databases/Transactions #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Atomic-классы.**

AtomicInteger, AtomicLong, AtomicReference. CAS (Compare-And-Swap) — атомарная инструкция CPU. Lock-free. Методы: get, set, compareAndSet, incrementAndGet. Для счётчиков с высоким contention — LongAdder (лучше масштабируется).

**Atomic-классы — как работают без блокировок?**

Через CAS (compare-and-swap) — атомарную инструкцию CPU. Lock-free. Классы: AtomicInteger, AtomicLong, AtomicReference.

**Atomic-классы — как работают без блокировок?**

Через CAS (compare-and-swap) — атомарную инструкцию процессора. Lock-free алгоритм.
