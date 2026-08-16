<!--
reps: 0
priority: 0
-->
#Databases/SQL/Transactions #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Уровни изоляции.**

READ_UNCOMMITTED — dirty read. READ_COMMITTED (default PG) — только закоммиченные. REPEATABLE_READ — повторное чтение = тот же результат. SERIALIZABLE — полная изоляция. Выше уровень → больше консистентности, меньше параллелизма, больше шанс deadlock.

**Уровни изоляции транзакций.**

READ_UNCOMMITTED, READ_COMMITTED (default в PostgreSQL), REPEATABLE_READ, SERIALIZABLE. От низкого к высокому: больше консистентности, меньше параллелизма.

**Уровни изоляции.**

READ_UNCOMMITTED, READ_COMMITTED (default в PostgreSQL), REPEATABLE_READ, SERIALIZABLE. От низкого к высокому: больше консистентности, меньше параллелизма.

**Какие уровни изоляции бывают?**

Read Uncommitted (можно читать незакоммиченные — dirty read). Read Committed (только закоммиченные, но возможен non-repeatable read). Repeatable Read (повторное чтение даст тот же результат, но возможен phantom read). Serializable (полная сериализация).

**Уровни изоляции транзакций.**

READ_UNCOMMITTED, READ_COMMITTED (default в PostgreSQL), REPEATABLE_READ, SERIALIZABLE. Защита от dirty/non-repeatable/phantom read.

**Уровни изоляции и какие проблемы решают.**

READ_UNCOMMITTED — dirty read. READ_COMMITTED — non-repeatable read. REPEATABLE_READ — phantom read. SERIALIZABLE — полная сериализация.

**Уровни изоляции.**

READ_UNCOMMITTED, READ_COMMITTED (default PG), REPEATABLE_READ, SERIALIZABLE. Аномалии: dirty/non-repeatable/phantom read.

**Уровни изоляции.**

READ_UNCOMMITTED, READ_COMMITTED (default PG), REPEATABLE_READ, SERIALIZABLE. Аномалии: dirty read, non-repeatable read, phantom read, serialization anomaly.

**What isolation levels does PostgreSQL actually provide?**

Источник: https://habr.com/ru/articles/968532/

Read Uncommitted: в PostgreSQL dirty read нет — ведёт себя как Read Committed.
Read Committed: каждый запрос видит данные, зафиксированные к моменту этого запроса, не к началу транзакции.
Repeatable Read: snapshot на старте транзакции; non-repeatable reads нет; в PostgreSQL нет и phantom reads.
Serializable: результат как при последовательном выполнении. Читатели не мешают друг другу; писатели блокируются только при изменении одного объекта.

**Postgres isolation cheat sheet?**

Default RC: new snapshot per statement. RR: one snapshot, no phantom in PG. Serializable: SSI, retry 40001. No dirty read.
