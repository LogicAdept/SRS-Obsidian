<!--
reps: 0
priority: 0
-->
#Java/Language #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Covering index — что это?**

Индекс, который содержит все поля запроса (через INCLUDE в PostgreSQL 11+). Позволяет Index Only Scan — без обращения к таблице.

**What is the difference between (user_id, status) and (user_id) INCLUDE (status)?**

Источник: https://habr.com/ru/articles/968532/

Составной (user_id, status): оба поля в ключе, сортировка user_id затем status; хорош для WHERE по user_id, по обоим, и для сортировки по ним.
INCLUDE: в ключе только user_id, status в листьях; сортировка только по user_id; покрывает запросы, где нужны оба поля, но не ищет/не сортирует по status отдельно.
INCLUDE обычно компактнее; составной гибче и лучше при фильтре по обоим полям. INCLUDE — PostgreSQL 11+, SQL Server и др.

**INCLUDE and Index Only Scan?**

B-tree (key) INCLUDE (payload). Needs visibility map. VACUUM. Expression indexes are not INCLUDE.

**Covering for list/search endpoints?**

All SELECT + WHERE cols in the index (INCLUDE). Index Only Scan. SELECT * kills it. Visibility map in Postgres. Search payload columns belong in INCLUDE, not as extra B-tree keys.
