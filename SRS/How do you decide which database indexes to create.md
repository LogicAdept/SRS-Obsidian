<!--
reps: 0
priority: 0
-->
#Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из шпаргалок Хабра (MishaBucha, 2025). Не сверен с официальной документацией. Не считать ответом для ревью.

**How do you decide which indexes to add?**

Источник: https://habr.com/ru/articles/968532/

Авторский алгоритм: цель (поиск/сортировка/join) → затраты vs выгода → анализ WHERE/ORDER BY → избегать индекса на каждое поле, делать составные на частые комбинации → порядок сортировки → уникальность → учитывать стоимость обновлений → мониторинг и пересмотр.

**Postgres index decision?**

EXPLAIN first. Partial for hot subset. Don't index JSONB blindly. Watch HOT and write amplification.

**Index from query shapes?**

Start from EXPLAIN of real queries. Equality, range, ORDER BY, JOIN keys, FK children. Partial for hot subset. Text search ≠ extra B-tree. Drop idx_scan=0. Writes pay for every index.
