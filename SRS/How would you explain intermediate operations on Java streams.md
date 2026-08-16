<!--
reps: 0
priority: 0
-->
#Java/Streams #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Stream API: промежуточные vs терминальные.**

Промежуточные (filter, map, flatMap, sorted, distinct, peek, limit, skip) — ленивые, возвращают Stream, не выполняются пока нет терминальной. Терминальные (collect, forEach, count, reduce, findFirst, toList) — запускают конвейер. Стрим одноразовый — после терминальной повторно нельзя.

**Stream API: промежуточные vs терминальные операции.**

Промежуточные (filter, map, sorted) возвращают Stream и ленивые. Терминальные (collect, forEach, count, reduce) запускают pipeline.

**Stream API: что такое, промежуточные vs терминальные.**

Stream — конвейер обработки данных. Промежуточные (ленивые): filter, map, flatMap, sorted. Терминальные (запускают): collect, forEach, count, reduce. Стрим одноразовый.

**Stream API: промежуточные vs терминальные операции. Что такое ленивость?**

Промежуточные (filter, map) не выполняются до вызова терминальной (collect, forEach).
