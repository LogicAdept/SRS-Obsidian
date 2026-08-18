<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/SQL/DDL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**What is EXCLUDE / exclusion constraint?**

EXCLUDE USING gist (room WITH =, during WITH &&) — no two rows with overlapping ranges for the same room. Booking/calendar classic. Needs GiST (or similar). Stronger than UNIQUE for 'no overlap' semantics.
