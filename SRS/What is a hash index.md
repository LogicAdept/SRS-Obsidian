<!--
reps: 0
priority: 0
-->
#Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из шпаргалок Хабра (MishaBucha, 2025). Не сверен с официальной документацией. Не считать ответом для ревью.

**What is a hash index?**

Источник: https://habr.com/ru/articles/968532/

Ключ—значение как словарь: хеш-таблица хранит адрес значения в файле. Чтение: посмотреть адрес и сходить в файл. Подходит для точного равенства, не для диапазонов.

**Postgres hash indexes?**

Equality only, WAL-logged since PG 10. Rarely better than B-tree; B-tree is the default answer.
