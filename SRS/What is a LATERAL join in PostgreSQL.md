<!--
reps: 0
priority: 0
-->
#Databases/PostgreSQL #Databases/SQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**What is LATERAL?**

Right-hand subquery/function can reference left-hand columns. Classic: top-N per group (LATERAL ... LIMIT) or unnest correlated. Without LATERAL, FROM items are independent. Interview alternative to window functions for 'latest N per parent'.

**LATERAL for top-N per parent?**

Per-row subquery with LIMIT uses an index (parent_id, ts DESC). Often beats a huge JOIN+ROW_NUMBER over the whole child table. Classic 'latest comments per post'.
