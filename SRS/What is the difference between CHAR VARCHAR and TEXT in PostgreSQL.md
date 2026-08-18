<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/SQL/DataTypes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**varchar(n) vs text?**

text and varchar without n are the same performance (TOAST). varchar(n) only adds a length check. char(n) pads — rarely wanted. Prefer text + CHECK if you need a limit. No 'varchar is faster' myth.
