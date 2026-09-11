<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**EXISTS for optimization?**

Semi-join; stop at first match. Prefer over NOT IN. Correlated EXISTS needs an index on the inner lookup columns. Often same plan as IN (SELECT ...) on modern engines.

**Что делает оператор `EXISTS`?**
`EXISTS` берет подзапрос, как аргумент, и оценивает его как `TRUE`, если подзапрос возвращает какие-либо записи и `FALSE`, если нет.
