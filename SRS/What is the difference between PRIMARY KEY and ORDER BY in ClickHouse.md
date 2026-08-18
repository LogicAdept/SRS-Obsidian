<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**PRIMARY KEY vs ORDER BY?**

ORDER BY = physical sort inside a part (compression + scan locality). PRIMARY KEY = sparse index; must be a prefix of ORDER BY. If omitted, PK = ORDER BY. Unlike SQL PK: duplicates allowed. You may ORDER BY (a,b,c) but PRIMARY KEY (a,b) to keep the index smaller.
