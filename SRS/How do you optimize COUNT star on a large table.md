<!--
reps: 0
priority: 0
-->
#Databases/SQL #SystemDesign/Performance #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**Why is COUNT(*) slow and what instead?**

COUNT(*) still visits lots of rows/visibility (MVCC). Approximate: reltuples / stats, cached counter table, HyperLogLog, covering index-only count of a narrow index. Filtered COUNT needs an index matching the WHERE. Don't COUNT(*) every request to render a pager.
