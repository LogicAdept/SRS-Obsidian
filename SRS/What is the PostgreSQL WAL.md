<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/Replication #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**What is WAL?**

Write-Ahead Log: changes hit WAL before data files (durability). Crash recovery replays WAL. Streaming replication ships WAL bytes. PITR = base backup + WAL archive. Segment ~16MB in pg_wal/. Sync commit vs async is a latency/RPO tradeoff. Don't fill the disk with unreplicated WAL (slots).
