<!--
reps: 0
priority: 0
-->
#Java/Collections/List #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**List.of(1,2,3) vs new ArrayList<>() — в чём разница?**

List.of возвращает неизменяемый список. add/remove бросают UnsupportedOperationException.
