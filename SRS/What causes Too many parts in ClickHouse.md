<!--
reps: 0
priority: 0
-->
#Databases/ClickHouse #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**What is the too-many-parts error?**

Inserts create parts faster than merges. Tiny INSERT (one row HTTP) is the classic. Fix: batch (thousands+), async_insert, Buffer table, fewer partitions, more merge threads as a bandage. Queries suffer before the error: each part has its own index/marks.
