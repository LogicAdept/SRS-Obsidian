<!--
reps: 0
priority: 0
-->
#Databases/ClickHouse #SystemDesign/Performance #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**Why does CH scan billions of rows faster than Postgres?**

Column files: read only selected columns. Compression on homogeneous data. Vectorized SIMD on blocks. Granule/partition skipping via ORDER BY and skip indexes. Postgres row store pays I/O for unused columns on wide facts.
