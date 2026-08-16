<!--
reps: 0
priority: 0
-->
#Databases/ClickHouse #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**Collapsing vs VersionedCollapsing?**

Sign +1/−1 rows cancel on merge (soft delete / state). Unpaired signs linger until a mate arrives. VersionedCollapsingMergeTree adds version for out-of-order inserts. Both need careful app protocol; FINAL or state-aware queries until merged.
