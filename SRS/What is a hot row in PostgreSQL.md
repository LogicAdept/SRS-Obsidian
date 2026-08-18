<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**What is a write-hot row and how do you fix it?**

One tuple updated by everyone (global counter). Updates serialize on the row lock; MVCC versions pile up. Shard the counter, buffer in Redis, or batch. Indexing the hot column also kills HOT. Classic interview failure mode.
