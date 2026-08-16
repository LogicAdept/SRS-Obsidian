<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**В `WeakHashMap` используются WeakReferences. А почему бы не создать `PhantomHashMap` на PhantomReferences?**

PhantomReference при вызове метода `get()` возвращает всегда `null`, поэтому тяжело представить назначение такой структуры данных.
