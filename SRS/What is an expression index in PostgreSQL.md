<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/Indexes/Functional #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**What is an expression / functional index?**

Index on (lower(email)) or ((data->>'id')). Query must use the same expression. JSONB path indexes are expression indexes — they often prevent HOT even if the JSON path didn't change. Immutable functions only.

**Expression index for search?**

lower(email), (data->>'sku'), to_tsvector(...). Query must use the same expression. Makes a previously non-sargable predicate sargable. Immutable functions only.
