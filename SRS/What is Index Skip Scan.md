<!--
reps: 0
priority: 0
-->
#Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**What is skip scan on a composite index?**

Some engines (MySQL 8+) can probe each distinct value of a missing leading column and then seek the rest — helps when the skipped column has few distinct values. Postgres generally wants the leftmost prefix (or a separate index). Don't quote skip-scan as universal.
