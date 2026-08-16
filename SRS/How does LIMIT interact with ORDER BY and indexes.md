<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**When does LIMIT use an index instead of a full sort?**

If ORDER BY matches an index (same direction, leftmost), the engine can stop after N rows (Index Scan + Limit). Mismatch → Sort of the whole set then Limit — death at scale. OFFSET still has to skip. Covering index avoids heap fetches on the hot path.
