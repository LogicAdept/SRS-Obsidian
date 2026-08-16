<!--
reps: 0
priority: 0
-->
#Databases/SQL #Security/AppSec/Injection #Problems/Persistence #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**SQL performance pitfalls?**

Non-sargable WHERE, SELECT *, OFFSET deep pages, NOT IN + NULL, correlated N+1, OR across columns, functions on indexed cols, DISTINCT to hide fan-out, COUNT(*) on every request.
