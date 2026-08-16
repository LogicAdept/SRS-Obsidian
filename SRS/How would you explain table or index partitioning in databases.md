<!--
reps: 0
priority: 0
-->
#Databases/Partitioning #Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из шпаргалок Хабра (MishaBucha, 2025). Не сверен с официальной документацией. Не считать ответом для ревью.

**What is table partitioning versus sharding?**

Источник: https://habr.com/ru/articles/968532/

Секционирование — деление таблицы внутри одной БД (например по месяцам). Упрощает поиск, данные остаются в одной БД, в отличие от шардирования.

**Postgres partitioning vs sharding?**

Declarative partitions in one cluster; prune by key. Sharding is multiple servers. Detach old partitions for retention.

**CH partitions vs PG partitions?**

CH PARTITION BY is folders + cheap DROP; ORDER BY is the real search skip. Over-partitioning creates too many parts. PG declarative partitions prune too but still have B-trees per partition.
