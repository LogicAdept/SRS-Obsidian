<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/SQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**What does ARRAY JOIN do?**

Explode array to rows (tags, Nested). Then GROUP BY tag. Cost: row multiplication. Nested(name, time) is parallel arrays of equal length. Useful for events-in-array models; don't explode then join huge dims without care.
