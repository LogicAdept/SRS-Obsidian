<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**Seq Scan vs Index Scan vs Bitmap Heap Scan vs Index Only Scan?**

Seq: whole heap. Index Scan: index then heap per tuple (random IO). Bitmap Index + Bitmap Heap: collect pages, read heap in order (lossy if work_mem small). Index Only: covering + visibility map. Nested Loop / Hash / Merge are joins, not scans.

**Which scan for a search?**

Seq: contains-search without trgm/FTS. Index: prefix/equality. Bitmap: moderately selective / multi-index. Index Only: covering list. GIN bitmap for FTS/trgm.
