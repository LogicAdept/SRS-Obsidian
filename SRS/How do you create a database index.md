<!--
reps: 0
priority: 0
-->
#Databases/Indexes #Databases/SQL #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Как создать индекс?**

Индекс можно создать либо с помощью выражения `CREATE INDEX`:
```sql
CREATE INDEX index_name ON table_name (column_name)
```

либо указав ограничение целостности в виде уникального `UNIQUE` или первичного `PRIMARY` ключа в операторе создания таблицы `CREATE TABLE`.

**Create the index the query can use?**

Match operators: B-tree for prefix/range, GIN/trgm for contains, expression for LOWER(). CONCURRENTLY in prod. Verify with EXPLAIN. One composite beats two unused singles for a hot pair.
