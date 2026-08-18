<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**Why does function volatility matter?**

IMMUTABLE: same args → same result forever — allowed in indexes. STABLE: constant within a statement (now() is STABLE). VOLATILE: anything (random, writes). Wrong IMMUTABLE → corrupt index. Planner inlines/caches based on this.
