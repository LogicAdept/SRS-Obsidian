<!--
reps: 0
priority: 0
-->
#Java/Collections/List/ArrayList #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**List.of(1,2,3) vs new ArrayList.**

List.of — immutable, add/remove → UnsupportedOperationException, null-элементы запрещены. ArrayList — обычный mutable список.
