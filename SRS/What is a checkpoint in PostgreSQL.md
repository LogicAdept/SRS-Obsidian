<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**What is a checkpoint?**

Flushes dirty buffers so recovery can start from a recent WAL location instead of replaying the whole log. Triggered by time (checkpoint_timeout), WAL volume (max_wal_size), or CHECKPOINT. Too frequent: extra IO. Too rare: long crash recovery. Distinct from VACUUM.
