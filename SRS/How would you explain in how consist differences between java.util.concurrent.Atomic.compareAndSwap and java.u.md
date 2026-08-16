<!--
reps: 0
priority: 0
-->
#Java/Concurrency #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**В чём заключаются различия между `java.util.concurrent.Atomic*.compareAndSwap()` и `java.util.concurrent.Atomic*.weakCompareAndSwap()`?**

+ `weakCompareAndSwap()` не создает _memory barrier_ и не дает гарантии _happens-before_;
+ `weakCompareAndSwap()` сильно зависит от кэша/CPU, и может возвращать `false` без видимых причин;
+ `weakCompareAndSwap()`, более легкая, но поддерживаемая далеко не всеми архитектурами и не всегда эффективная операция.
