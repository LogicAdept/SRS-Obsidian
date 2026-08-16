<!--
reps: 0
priority: 0
-->
#Databases/SQL #SystemDesign/Performance #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**What does a disk sort mean?**

Sort did not fit in work_mem / sort_buffer — spilled to temp files. Increase memory carefully (per operation × connections), or add an index to avoid the sort, or reduce rows before ORDER BY. EXPLAIN ANALYZE / BUFFERS shows temp reads.
