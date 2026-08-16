<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**What is Bitmap Heap Scan for?**

Index(es) produce a bitmap of heap pages, then heap is read in physical order (less random I/O). Good for moderate selectivity or AND/OR of several indexes. Lossy bitmap if work_mem is tight (recheck). Different from a single Index Scan of a very selective key.
