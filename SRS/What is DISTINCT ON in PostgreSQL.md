<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/SQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**What is DISTINCT ON?**

Postgres extension: DISTINCT ON (user_id) keep one row per user, first according to ORDER BY. Classic 'latest row per group' without a window. ORDER BY must start with the ON expressions. Not standard SQL.
