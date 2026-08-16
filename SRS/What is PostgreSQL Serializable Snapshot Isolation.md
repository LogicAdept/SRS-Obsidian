<!--
reps: 0
priority: 0
-->
#Databases/PostgreSQL #Databases/SQL/Transactions #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**How does SERIALIZABLE work in Postgres?**

SSI: snapshot isolation plus predicate conflict detection. May throw serialization_failure — retry the transaction. Repeatable Read in PG already avoids phantoms via snapshots; Serializable adds write-skew protection. Default remains Read Committed.
