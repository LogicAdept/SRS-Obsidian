<!--
reps: 0
priority: 0
-->
#Databases/Indexes/Covering #Databases/Relational/PostgreSQL #Databases/Indexes/Composite #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из шпаргалок Хабра (MishaBucha, 2025). Не сверен с официальной документацией. Не считать ответом для ревью.

**Composite index vs INCLUDE covering index?**

Источник: https://habr.com/ru/articles/968532/

Составной: оба поля в ключе, поддерживает поиск и сортировку по префиксу и по обоим. INCLUDE: второе поле только в листьях (покрывающий), индекс меньше, но status сам по себе не ключ поиска. Для фильтра по обоим полям составной обычно лучше.

**Composite vs INCLUDE recap?**

Composite keys sort and can search prefix. INCLUDE columns don't search as keys. INCLUDE smaller when you only need extra cols for IOS.

**Composite vs INCLUDE for filters?**

Key columns search and sort. INCLUDE only payload for IOS. Don't put a low-value filter column last if you never search it as a key — INCLUDE it.
