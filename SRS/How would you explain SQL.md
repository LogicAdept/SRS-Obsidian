<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Какие группы команд SQL ты знаешь?**

DML (Data Manipulation Language) — работа с данными: SELECT, INSERT, UPDATE, DELETE. DDL (Data Definition Language) — структура: CREATE, ALTER, DROP. DCL (Data Control Language) — права: GRANT, REVOKE. TCL (Transaction Control Language) — управление транзакциями: COMMIT, ROLLBACK, SAVEPOINT.

**SQL on Postgres specifically?**

Declarative; planner picks scans/joins. Postgres extras: DISTINCT ON, RETURNING, JSONB, arrays, LISTEN, extensions. Cost of MVCC still applies.
