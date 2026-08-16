<!--
reps: 0
priority: 0
-->
#Databases/Indexes #Databases/SQL #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Типы индексов PostgreSQL.**

B-tree (default) — =, <, >, BETWEEN, ORDER BY, LIKE 'abc%'. Hash — только =. GIN — массивы, JSONB, full-text. GiST — геометрия, диапазоны. BRIN — большие таблицы с порядком (timestamp). Покрывающий индекс (INCLUDE) — добавляет колонки в лист, Index Only Scan.

**Когда индекс НЕ поможет?**

Маленькие таблицы. Низкая selectivity (boolean). Функции (LOWER(email) — нужен expression index). LIKE '%abc' (wildcard в начале). Часто обновляемые колонки (индекс замедляет INSERT/UPDATE/DELETE).

**Зачем нужны индексы?**

Чтобы ускорить поиск. Без индекса — full scan O(n). С B-tree индексом — O(log n). Платим за это: дополнительная память + замедление INSERT/UPDATE/DELETE.

**Когда индекс не стоит создавать?**

Маленькие таблицы (full scan быстрее). Часто меняющиеся колонки. Колонки с малым количеством уникальных значений (например, boolean) — индекс не даст выигрыша.

**Типы индексов в PostgreSQL.**

B-tree (default — =, <, >, BETWEEN, ORDER BY), Hash (только =), GIN (массивы, JSONB, full-text), GiST (геометрия), BRIN (большие таблицы с порядком), SP-GiST.

**Когда индекс НЕ стоит создавать?**

Маленькие таблицы (full scan быстрее). Колонки с малым числом уникальных значений (boolean, enum с 2–3 значениями). Часто меняющиеся колонки — индекс замедлит INSERT/UPDATE/DELETE.

**Что такое индекс? Зачем он нужен?**

Структура данных (обычно B-tree), позволяющая БД быстро находить строки по значениям колонок. Без индекса — Seq Scan (полный обход таблицы). С индексом — поиск за O(log n).

**Какие виды индексов есть?**

B-tree (по умолчанию, для =, <, >, BETWEEN, LIKE 'abc%'). Hash (только =, в Postgres есть, но используется редко). GIN — для массивов, JSONB, full-text. GiST — геометрия, диапазоны. BRIN — для огромных таблиц с естественной упорядоченностью (временные ряды).

**Почему нельзя на все поля навесить индексы?**

(1) Каждый индекс нужно обновлять при INSERT/UPDATE/DELETE — замедление записи. (2) Индексы занимают место — на больших таблицах могут весить больше самой таблицы. (3) Они требуют обслуживания (VACUUM, REINDEX). Правило: индексы только на колонки, по которым реально часто фильтруют, сортируют, джойнят.

**Типы индексов в PostgreSQL.**

B-tree (default, для =, <, >, BETWEEN), Hash (только =), GIN (массивы, JSONB), GiST (геометрия), BRIN (большие таблицы с порядком), SP-GiST.

**Два одинарных индекса vs один составной — что лучше?**

Зависит от запроса. WHERE a=1 AND b=2: составной (a,b) — один Index Scan. Два одинарных: Bitmap Index Scan + Bitmap AND — медленнее. WHERE a=1 OR b=2: два одинарных — Bitmap OR. Составной (a,b) не поможет для WHERE b=2 (leftmost prefix). Общее правило: составной для AND-запросов, одинарные для OR или независимых WHERE.

**Кейс: «навесили индексов на все поля — запись стала медленнее».**

Каждый INSERT/UPDATE/DELETE обновляет ВСЕ индексы. 10 индексов = 10x overhead на запись. VACUUM тоже замедляется. REINDEX может понадобиться. Решение: индексы только по паттернам запросов (WHERE, JOIN, ORDER BY). Мониторинг: pg_stat_user_indexes → проверить idx_scan (сколько раз использовался).

**Почему Tree индекс в БД, а не Hash?**

Хотя Hash = O(1), Tree (B-tree) поддерживает диапазонные запросы, сортировку, BETWEEN, LIKE 'abc%'. Hash — только точное совпадение.

**Индексы PostgreSQL.**

B-tree (default), Hash, GIN (JSONB, full-text), GiST (геометрия), BRIN (большие таблицы). Покрывающий (INCLUDE).

**Порядок колонок в составном индексе.**

Leftmost prefix rule. INDEX (a, b, c) используется для WHERE a=, WHERE a= AND b=, но НЕ для WHERE b= или WHERE c=.

**Типы индексов PostgreSQL.**

B-tree (default), Hash (=), GIN (JSONB, full-text), GiST (геометрия), BRIN (большие таблицы с порядком). Покрывающий индекс (INCLUDE) — Index Only Scan.

**What is a database index and what is the cost?**

Источник: https://habr.com/ru/articles/968532/

Вспомогательная структура рядом с таблицей, ускоряет поиск. Замедляет INSERT/UPDATE/DELETE, потому что индекс тоже нужно обновлять.

**Postgres cost of indexes?**

Faster reads, slower writes, extra WAL. HOT fails if indexed columns change. Partial indexes cut write cost.

**Index vs heap for optimization?**

B-tree seek + possible heap fetch. Covering avoids heap. Random heap I/O can beat seq scan only when few rows. Search '%x%' does not seek a B-tree.
