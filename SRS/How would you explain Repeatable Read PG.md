<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Repeatable Read в PG решает фантомное чтение — почему?**

В стандарте SQL Repeatable Read допускает phantom reads. В PG благодаря MVCC (snapshot isolation): транзакция видит snapshot данных на момент начала. Новые строки, вставленные другими транзакциями, не видны → нет фантомов. Но: при попытке UPDATE конфликтующей строки — serialization failure → retry.
