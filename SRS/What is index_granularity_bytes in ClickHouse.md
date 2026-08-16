<!--
reps: 0
priority: 0
-->
#Databases/ClickHouse #Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**Adaptive granularity?**

Besides 8192 rows, adaptive size in bytes can split fat rows into smaller granules so skip indexes/PK marks stay useful on wide events. Interview depth: marks are not only 'every 8192 rows' on modern versions.
