<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SystemDesign/Reliability #SystemDesign/Availability #DistributedSystems #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**HA vs CDC?**

Streaming physical for HA/read replicas. Logical for subset/CDC. Sync vs async RPO. Slots retain WAL.
