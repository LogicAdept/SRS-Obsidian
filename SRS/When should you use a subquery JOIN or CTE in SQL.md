<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Подзапрос vs JOIN vs CTE — когда что?**

Подзапрос: в WHERE для фильтрации (WHERE id IN (SELECT ...)). JOIN: для объединения данных из нескольких таблиц. CTE (WITH ... AS): для читаемости сложных запросов, рекурсия. Коррелированный подзапрос: выполняется для каждой строки внешнего запроса (медленно). Для AQA: CTE упрощает отладку — можно запустить каждую часть отдельно.

**CTE vs subquery vs join for optimization?**

PG12+ inlines CTEs unless MATERIALIZED. Forced materialize can hide indexes. Prefer join/EXISTS when the optimizer can push filters. Recursive CTE is the exception.
