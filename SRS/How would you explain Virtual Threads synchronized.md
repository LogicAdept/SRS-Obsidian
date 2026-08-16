<!--
reps: 0
priority: 0
-->
#Java/Concurrency #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Virtual Threads и synchronized.**

Virtual Thread на synchronized → pinning (привязка к platform thread). Решение: ReentrantLock вместо synchronized. Это частый вопрос для Java 21.
