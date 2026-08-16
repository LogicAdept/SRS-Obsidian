<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Каков общий синтаксис оператора `SELECT`?**

`SELECT` - оператор DML SQL, возвращающий набор данных (выборку) из базы данных, удовлетворяющих заданному условию. Имеет следующую структуру:

```sql
SELECT
       [DISTINCT | DISTINCTROW | ALL]
       select_expression,...
   FROM table_references
     [WHERE where_definition]
     [GROUP BY {unsigned_integer | column | formula}]
     [HAVING where_definition]
     [ORDER BY {unsigned_integer | column | formula} [ASC | DESC], ...]
```
