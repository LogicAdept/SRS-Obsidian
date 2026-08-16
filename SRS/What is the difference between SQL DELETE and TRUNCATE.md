<!--
reps: 0
priority: 0
-->
#Databases/SQL/DML #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**DELETE vs TRUNCATE.**

DELETE — построчно, триггеры, WAL, можно WHERE, можно откатить. TRUNCATE — мгновенная очистка, сброс автоинкремента, не пишет каждую строку в WAL.

**Чем отличается DELETE от TRUNCATE?**

DELETE — построчное удаление с триггерами и логированием, может быть откачено в транзакции. TRUNCATE — быстрая очистка таблицы целиком, обнуляет автоинкремент.

**DELETE vs TRUNCATE.**

DELETE — построчное удаление с триггерами и WAL, можно откатить в транзакции. TRUNCATE — быстрая очистка целиком, сбрасывает счётчики автоинкремента.

**DELETE vs TRUNCATE in Postgres?**

DELETE: row WAL, triggers, WHERE, MVCC dead tuples. TRUNCATE: DDL, exclusive, resets identity, FK CASCADE needed. DROP removes the table.
