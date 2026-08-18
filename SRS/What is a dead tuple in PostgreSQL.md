<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**What is a dead tuple?**

Old row version no longer visible to any running transaction (after UPDATE/DELETE commit and snapshots move on). Still occupies heap until VACUUM marks the space reusable. Indexes may still point at it until cleaned. Too many → bloat and slow seq scans.
