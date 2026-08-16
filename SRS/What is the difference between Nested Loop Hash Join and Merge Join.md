<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**Nested Loop vs Hash Join vs Merge Join?**

Nested Loop: per outer row, inner lookup — needs index on inner, small outer. Hash Join: build hash of one side, probe — large equi-joins, needs work_mem or spills. Merge Join: both sorted on key (index or explicit Sort). Nested Loop × huge loops = bad estimate. Read loops × time.
