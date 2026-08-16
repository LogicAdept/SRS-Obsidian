<!--
reps: 0
priority: 0
-->
#Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**Bitmap AND / OR of indexes?**

Planner can AND/OR bitmaps from two single-column indexes instead of one composite. Composite is usually better for a frequent pair (a,b). Two indexes more flexible for mixed workloads, worse for that hot pair. EXPLAIN: BitmapAnd / BitmapOr.
