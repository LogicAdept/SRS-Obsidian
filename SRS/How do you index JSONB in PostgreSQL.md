<!--
reps: 0
priority: 0
-->
#Databases/PostgreSQL #Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**How do you index JSONB?**

GIN jsonb_ops (contains @>) or jsonb_path_ops. Expression B-tree on (data->>'status') for equality. GIN is write-heavy. Containment queries match GIN; don't expect B-tree on arbitrary nested paths without an expression.

**JSONB search without seq scan?**

GIN @> or expression B-tree on extracted keys. LIKE on jsonb::text is a full parse. Hot search fields → real columns.
