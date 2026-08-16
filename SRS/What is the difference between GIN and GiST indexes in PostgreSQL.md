<!--
reps: 0
priority: 0
-->
#Databases/PostgreSQL #Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**GIN vs GiST?**

GIN: inverted, exact containment — JSONB @>, arrays, FTS lexemes. Write-heavier, pending list. GiST: generalized tree, lossy possible — geometry, ranges, nearest-neighbor, some FTS. Interview: JSONB containment → GIN; PostGIS / overlaps → GiST.
