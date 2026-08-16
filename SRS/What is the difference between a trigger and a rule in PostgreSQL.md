<!--
reps: 0
priority: 0
-->
#Databases/PostgreSQL #Databases/SQL/DDL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**TRIGGER vs RULE?**

Triggers: per-row or per-statement functions on INSERT/UPDATE/DELETE (and some DDL via event triggers). Rules: query rewrite, historically for views; easy to surprise. Prefer INSTEAD OF triggers on views and ordinary triggers on tables. Don't invent RULE-based ORM magic.
