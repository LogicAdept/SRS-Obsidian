<!--
reps: 0
priority: 0
-->
#Java/Streams #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Какие операции бывают в Stream?**

Промежуточные (intermediate) — возвращают Stream, lazy: filter, map, flatMap, distinct, sorted, peek. Терминальные (terminal) — запускают конвейер: collect, reduce, forEach, count, findFirst. Без терминальной операции Stream НЕ выполняется.
