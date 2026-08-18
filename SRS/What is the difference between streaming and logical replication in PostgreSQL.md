<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/Replication #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**Physical/streaming vs logical replication?**

Streaming: WAL bytes, whole instance (almost), same major version typically, replica is binary clone, fast HA. Logical: row changes via decoding, subset of tables, cross-version, CDC (Debezium). Logical: no DDL (mostly), sequences need care, heavier on big writes. Interview: HA replica vs selective sync/CDC.
