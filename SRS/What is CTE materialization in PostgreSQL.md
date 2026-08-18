<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/SQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**Do CTEs always materialize?**

Historically WITH was an optimization fence (always materialize). PG 12+: inlined by default unless MATERIALIZED / used twice / has side effects. Can hide indexes if you force materialize. Interview: 'CTE made it slow' often this.

**CTE fence vs search filters?**

MATERIALIZED CTE can block pushing a LIKE/equality into the base scan. PG12+ inlines by default. If a search filter sits outside a CTE, check whether it was pushed down.
