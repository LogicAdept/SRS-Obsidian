<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**What is a projection?**

A stored alternate ORDER BY (and optional aggregation) for the same table. Planner may read the projection when it matches the query — second sparse index without a separate table. Cost: extra disk and merge work. Alternative to a second MV when you need another search key (e.g. by user_id vs by url).
