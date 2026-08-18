<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/SQL/DML #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**What is ON CONFLICT (UPSERT)?**

INSERT ... ON CONFLICT (pk) DO UPDATE/NOTHING. Needs a unique constraint/index to conflict on. Partial unique indexes work with matching inference. Race-safe vs SELECT-then-INSERT. RETURNING for the row. Don't use for high-churn JSON blobs without thinking HOT.
