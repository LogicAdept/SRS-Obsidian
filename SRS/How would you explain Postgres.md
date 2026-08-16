<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**В Postgres какой уровень по умолчанию?**

Read Committed. В Postgres вообще нет Read Uncommitted — это его особенность. Repeatable Read в Postgres ДОПОЛНИТЕЛЬНО защищает от phantom read через MVCC.

**Default isolation and MVCC one-liner?**

ORDBMS, ACID, MVCC. Default Read Committed; Read Uncommitted = Read Committed. Extensible types, JSONB, arrays, FTS.
