<!--
reps: 0
priority: 0
-->
#Java/Language #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**В чём отличие MATERIALIZED VIEW?**

Хранит результат запроса физически. Быстрее на чтение, но нужно периодически обновлять (REFRESH). Используется для тяжёлых аналитических запросов.

**Materialized view in Postgres?**

Stored result; REFRESH (CONCURRENTLY needs unique index). Stale until refresh. Not incremental natively. Use for heavy aggregates; RLS/views for live abstraction.

**Postgres MV vs ClickHouse MV?**

PG: stored snapshot, REFRESH. CH default MV: INSERT trigger into another table. Refreshable CH MVs exist for snapshots. Don't assume ON SELECT.
