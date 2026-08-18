<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/SQL/Transactions #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**FOR UPDATE vs FOR SHARE?**

FOR UPDATE: exclusive row lock, blocks other writers and other FOR UPDATE/SHARE. FOR SHARE: shared, many readers, still blocks UPDATE/DELETE. Use SHARE when you only need the row to stay put while you read related data. SKIP LOCKED / NOWAIT apply to both.
