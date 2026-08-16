<!--
reps: 0
priority: 0
-->
#Databases/PostgreSQL #Databases/SQL/Transactions #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**What is SAVEPOINT?**

Nested rollback inside a transaction: ROLLBACK TO savepoint keeps the outer tx. Used for retrying a statement without aborting the whole tx. Not a second connection. Heavy use in loops is a smell.
