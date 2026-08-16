<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Какие виды JOIN ты знаешь?**

INNER JOIN — пересечение. LEFT JOIN — все из левой + совпадения. RIGHT JOIN — наоборот. FULL OUTER JOIN — всё.

**Виды JOIN.**

INNER — пересечение. LEFT — все из левой + совпадения из правой. RIGHT — наоборот. FULL OUTER — всё. CROSS — декартово произведение.

**Какие виды JOIN ты знаешь?**

INNER JOIN — только совпадения из обеих таблиц. LEFT JOIN — все строки из левой + совпадения из правой (несовпадения = NULL). RIGHT JOIN — наоборот. FULL OUTER JOIN — все строки из обеих, несовпадения = NULL. CROSS JOIN — декартово произведение.

**Join methods in Postgres plans?**

Nested Loop (small outer), Hash Join (equi, needs work_mem), Merge Join (sorted). LATERAL for correlated. FK indexes make NL viable.

**Join method choice?**

NL + index on inner; Hash for large equi; Merge if sorted. Fan-out on 1:N. Anti/semi joins for existence. Functions in ON kill indexes.
