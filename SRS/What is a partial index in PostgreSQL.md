<!--
reps: 0
priority: 0
-->
#Databases/PostgreSQL #Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**What is a partial index?**

CREATE INDEX ... WHERE status = 'open'. Smaller, cheaper writes, matches queries with that predicate. Classic: index unpaid invoices, not the whole history. Planner must see the same condition (or implied).

**Partial index for search/filters?**

Index WHERE status IN ('open','new') — smaller, cheaper writes, matches those queries. Great for 'active only' search. Planner must see the same predicate (or infer it).
