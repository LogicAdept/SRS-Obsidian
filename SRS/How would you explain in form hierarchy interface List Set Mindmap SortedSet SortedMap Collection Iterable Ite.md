<!--
reps: 0
priority: 0
-->
#Java/Collections #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Расположите в виде иерархии следующие интерфейсы: `List`, `Set`, `Mindmap`, `SortedSet`, `SortedMap`, `Collection`, `Iterable`, `Iterator`, `NavigableSet`, `NavigableMap`.**

+ `Iterable`
    + `Collection`
        + `List`
        + `Set`
            + `SortedSet`
                + `NavigableSet`
+ `Mindmap`
    + `SortedMap`
        + `NavigableMap`
+ `Iterator`
