<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Для чего используется оператор `GROUP BY`?**

`GROUP BY` используется для агрегации записей результата по заданным признакам-атрибутам.

**GROUP BY vs window in Postgres?**

GROUP BY collapses rows. Window keeps them. FILTER, GROUPING SETS. Same NULL-as-one-group rule.
