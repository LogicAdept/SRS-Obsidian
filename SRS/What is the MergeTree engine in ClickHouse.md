<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**What is MergeTree?**

Default family: INSERT writes an immutable sorted part; background merges compact parts and apply engine logic (replace/sum/collapse). ORDER BY + optional PARTITION BY + sparse primary index. Variants: Replicated, Replacing, Summing, Aggregating, Collapsing.
