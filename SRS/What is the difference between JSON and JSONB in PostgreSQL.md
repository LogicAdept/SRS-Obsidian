<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/SQL/DataTypes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**JSON vs JSONB?**

JSON: text, preserves whitespace/key order, reparsed. JSONB: binary, dedup keys, indexable (GIN), faster read. Prefer JSONB. Updates rewrite the whole value → no HOT if GIN/expression indexes exist. Pull hot filter fields into columns.
