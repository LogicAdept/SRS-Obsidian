<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**What if estimated rows and actual rows differ a lot?**

Planner costs the wrong join/scan (Nested Loop on millions of rows). ANALYZE / autoanalyze; raise statistics target on skewed columns; CREATE STATISTICS for correlated cols. After bulk load, ANALYZE immediately. EXPLAIN ANALYZE is how you see the lie.
