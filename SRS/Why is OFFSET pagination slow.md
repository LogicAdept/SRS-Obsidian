<!--
reps: 0
priority: 0
-->
#Databases/SQL #SystemDesign/Performance #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**Why is LIMIT 20 OFFSET 100000 expensive?**

Engine still walks/skips the discarded rows (even with an index). Cost grows with page number. Also unstable under inserts (duplicates/skips). Fine for tiny admin UIs. Production feeds: keyset/cursor. COUNT(*) for total pages is a second sequential tax.
