<!--
reps: 0
priority: 0
-->
#Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**Clustered vs secondary for lookups?**

Clustered (InnoDB PK): table order. Secondary: extra lookup. Postgres heap + all secondary. CLUSTER is a one-shot reorder. Point lookup by PK is the clustered win in MySQL.
