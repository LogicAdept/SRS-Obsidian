<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/PostgreSQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**VACUUM jobs?**

Reclaim dead tuples, FSM, visibility map (index-only), freeze wraparound, ANALYZE if requested. Autovacuum. FULL = rewrite + exclusive lock.
