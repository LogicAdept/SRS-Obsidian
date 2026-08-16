<!--
reps: 0
priority: 0
-->
#Databases/PostgreSQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**pg_dump vs pg_basebackup?**

pg_dump: logical SQL/custom, per DB, easy, not PITR by itself. pg_basebackup: physical, whole cluster, with WAL archive → PITR. Managed clouds: snapshots + PITR. Test restores. Slots/replication for HA is not a backup.
