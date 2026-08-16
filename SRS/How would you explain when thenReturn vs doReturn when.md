<!--
reps: 0
priority: 0
-->
#Java/Language #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**when/thenReturn vs doReturn/when.**

when(x.method()).thenReturn(y) — стандартный способ. doReturn(y).when(x).method() — нужен для spy (иначе вызовется реальный метод) и для void-методов.
