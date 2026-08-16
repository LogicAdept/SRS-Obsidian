<!--
reps: 0
priority: 0
-->
#Databases/PostgreSQL #Databases/SQL/DataTypes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**timestamp vs timestamptz?**

timestamptz stores an instant (UTC internally, converts on display). timestamp without time zone is a wall-clock with no zone — easy to mix offsets. Prefer timestamptz for events. Date-only holidays can be date. Session TimeZone matters for display.
