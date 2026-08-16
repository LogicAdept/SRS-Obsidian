<!--
reps: 0
priority: 0
-->
#Databases/PostgreSQL #Databases/SQL/Transactions #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**Does Postgres Repeatable Read allow phantoms?**

Standard SQL RR still allows phantoms. Postgres RR uses a single snapshot for the whole transaction, so new committed rows from others are invisible — no phantoms. Write skew still possible until SERIALIZABLE (SSI, retry 40001). Default remains Read Committed.
