<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**В PostgreSQL нет Read Uncommitted — почему?**

Минимальный уровень — Read Committed. PostgreSQL использует MVCC: каждая транзакция видит snapshot, грязные данные физически невозможно прочитать (нет dirty read). Read Uncommitted в PG ведёт себя как Read Committed. Любят спрашивать — это особенность PG.

**Does PostgreSQL support dirty reads?**

Источник: https://habr.com/ru/articles/968532/

Фактически нет. Любые SELECT видят только зафиксированные данные, даже при Read Uncommitted — он ведёт себя как Read Committed.

**Does Postgres dirty-read?**

No. READ UNCOMMITTED is an alias for READ COMMITTED. Dirty reads are not implemented.
