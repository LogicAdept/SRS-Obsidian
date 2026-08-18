<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**What is XID wraparound?**

XIDs are 32-bit. If they wrap, old tuples can look in the future and vanish. Freeze marks old tuples with a special XID. autovacuum_freeze_max_age (~200M) forces freeze vacuum. Emergency stop if age gets critical. Long transactions and disabled autovacuum cause this outage class.
