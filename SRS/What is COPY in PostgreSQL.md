<!--
reps: 0
priority: 0
-->
#Databases/PostgreSQL #Databases/SQL/DML #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**COPY vs INSERT?**

COPY (or \copy) bulk-loads, far fewer round trips than row INSERTs. Disable/rebuild indexes and FK checks for huge loads when safe. CSV/binary. App: batched INSERT still OK; COPY for migrations/ETL.
