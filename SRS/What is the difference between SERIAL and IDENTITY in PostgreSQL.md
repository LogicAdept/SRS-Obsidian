<!--
reps: 0
priority: 0
-->
#Databases/PostgreSQL #Databases/SQL/DataTypes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**SERIAL vs GENERATED AS IDENTITY?**

SERIAL: legacy int/bigint + sequence + default; ownership quirks on dump/restore. IDENTITY (PG 10+): SQL-standard, preferred. Sequences have gaps after rollback — never use as gapless invoice numbers. UUID v7 if you need distributed time-ordered keys.
