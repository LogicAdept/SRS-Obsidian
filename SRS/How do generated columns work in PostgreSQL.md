<!--
reps: 0
priority: 0
-->
#Databases/PostgreSQL #Databases/SQL/DDL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**What are generated columns?**

STORED column computed from others (PG 12+). Indexable. VIRTUAL later versions. Alternative to expression indexes when you query the value often. Must be immutable expressions.
