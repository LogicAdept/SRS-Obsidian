<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/Replication #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**What is a replication slot?**

Primary retains WAL until the replica/consumer consumed it. Protects against removing WAL too soon; can fill the disk if the replica dies. Monitor pg_replication_slots restart_lsn lag. Logical slots for CDC.
