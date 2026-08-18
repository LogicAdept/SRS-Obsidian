<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/Indexes #Databases/Relational/PostgreSQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**How do you index a search inside JSON?**

Don't seq-scan JSON text with LIKE. JSONB: GIN jsonb_path_ops for @>, or expression B-tree on (data->>'sku') for equality. Generated/stored columns for hot keys. LIKE '%x%' on a JSON dump is the worst of both worlds. Pull searchable fields out if they are stable.
