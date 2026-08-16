<!--
reps: 0
priority: 0
-->
#Databases/PostgreSQL #Databases/Transactions #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**What is MVCC and why does it matter?**

Multi-Version Concurrency Control: UPDATE/DELETE create a new tuple version (xmin/xmax) instead of overwriting. Readers see a snapshot; readers don't block writers and writers don't block readers. Cost: dead tuples, bloat, VACUUM, long transactions freeze cleanup. Interview: this is the Postgres depth check.
