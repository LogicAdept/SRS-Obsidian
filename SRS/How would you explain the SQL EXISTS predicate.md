<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**EXISTS for optimization?**

Semi-join; stop at first match. Prefer over NOT IN. Correlated EXISTS needs an index on the inner lookup columns. Often same plan as IN (SELECT ...) on modern engines.
