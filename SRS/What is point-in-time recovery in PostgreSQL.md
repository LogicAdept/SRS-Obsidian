<!--
reps: 0
priority: 0
-->
#Databases/PostgreSQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**What is PITR?**

Restore a base backup, replay WAL up to a timestamp/LSN. Needs archive_mode + wal_level and archived segments. Distinct from a single dump. Interview: backup without WAL archive is not PITR.
