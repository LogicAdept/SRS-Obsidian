<!--
reps: 0
priority: 0
-->
#Databases/Transactions #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**MVCC.**

Каждая строка: xmin (создавшая транзакция), xmax (удалившая/обновившая). Читатели не блокируют писателей. Snapshot isolation. Старые версии чистит VACUUM (autovacuum). Проблема: table bloat если VACUUM не успевает.

**MVCC generally vs Postgres?**

Concurrency via versions not read locks. Postgres stores versions in the heap (not undo log like Oracle/InnoDB). That's why VACUUM exists.
