<!--
reps: 0
priority: 0
-->
#Databases/PostgreSQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**What does autovacuum do?**

Background workers VACUUM/ANALYZE when dead tuples pass a threshold (scale_factor + threshold). Also freeze to prevent XID wraparound — wraparound vacuum can run even if you 'disable' autovacuum. Tune per busy tables. Never disable globally. Watch pg_stat_user_tables n_dead_tup and wraparound age.
