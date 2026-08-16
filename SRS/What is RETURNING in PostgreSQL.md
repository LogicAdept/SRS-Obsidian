<!--
reps: 0
priority: 0
-->
#Databases/PostgreSQL #Databases/SQL/DML #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**What is RETURNING?**

INSERT/UPDATE/DELETE ... RETURNING * (or cols) gives the new/old row in one round trip. UPSERT + RETURNING is the idiom. Triggers still fire.
