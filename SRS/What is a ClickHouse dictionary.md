<!--
reps: 0
priority: 0
-->
#Databases/ClickHouse #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**Dictionaries vs JOIN?**

In-memory KV from a table/MySQL/file. dictGet at query time instead of joining a dimension. Refresh periodically. Right for countries, plans, user flags — not for unbounded facts. Faster and stabler than GLOBAL JOIN of a big right table.
