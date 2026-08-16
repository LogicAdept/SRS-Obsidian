<!--
reps: 0
priority: 0
-->
#Java/Language #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Реализуй ограниченную BlockingQueue.**

synchronized + wait/notify. while(!condition) wait() — не if! (spurious wakeups). put() ждёт если полная, take() ждёт если пустая. notifyAll() после каждой операции.
