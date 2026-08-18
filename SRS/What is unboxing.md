<!--
reps: 0
priority: 0
-->
#Java/Language/Wrappers #Java/Language/Primitives #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Что такое автобоксинг и unboxing? В чём подвох?**

Автоматическое преобразование примитива в обёртку и обратно: Integer i = 5; — это int 5 заворачивается в Integer (boxing). int j = i; — обратно (unboxing). Подвох в том, что если обёртка null, при unboxing будет NullPointerException: Integer i = null; int j = i; — НПЕ.
