<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**MVCC в PostgreSQL — как работает?**

Каждая транзакция видит snapshot БД. Вместо изменений — новые версии строк (xmin/xmax). Старые чистит VACUUM.

**MVCC в PostgreSQL — как работает?**

Каждая транзакция видит snapshot базы. Вместо изменений — новые версии строк с xmin/xmax. Старые версии чистит VACUUM.

**MVCC в PostgreSQL.**

Каждая строка: xmin (создавшая транзакция), xmax (удалившая). Читатели не блокируют писателей. Старые версии чистит VACUUM. Проблема: table bloat.

**MVCC snapshot recap?**

Snapshot per tx/statement; new versions on write; VACUUM reclaims. Long tx block cleanup.
