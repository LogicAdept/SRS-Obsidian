<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/Keys #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**UUID vs bigint PK?**

UUID v4: random, fragments B-tree, fatter indexes. UUID v7 / ULID: time-ordered, nicer inserts. bigint identity: small, sequential, fast. External IDs can be UUID without being the clustering key. Interview: random UUID PK + high insert rate = page splits.
