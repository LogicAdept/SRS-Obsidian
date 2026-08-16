<!--
reps: 0
priority: 0
-->
#DSA/DataStructures/Tree/BTree #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из шпаргалок Хабра (MishaBucha, 2025). Не сверен с официальной документацией. Не считать ответом для ревью.

**How does a B-tree index work?**

Источник: https://habr.com/ru/articles/968532/

Самая распространённая индексная структура. Ключ—значение отсортированы (как SSTable), плюс диапазонные запросы. Данные на страницах фиксированного размера (~4 КБ). Поиск с корня вниз по диапазонам ключей.

**B-tree in Postgres?**

Default index. Equality, range, ORDER BY, LIKE 'prefix%'. Leftmost prefix on composites. Not for '%foo%' (pg_trgm/GIN) or JSONB containment (GIN).

**B-tree for SQL search?**

Ordered keys: = < > BETWEEN LIKE 'pre%'. Not '%infix%'. Range and ORDER BY. Hash is equality-only. GIN/trigram/FTS for other search.
