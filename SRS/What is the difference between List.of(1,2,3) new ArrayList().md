<!--
reps: 0
priority: 0
-->
#Java/Collections/List/ArrayList #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**В чём разница между List.of(1,2,3) и new ArrayList<>()?**

List.of возвращает immutable-список. Любая попытка изменить — UnsupportedOperationException. И в нём нельзя null.
