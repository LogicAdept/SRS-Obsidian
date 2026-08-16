<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**How do you read cost, rows, actual time, loops?**

cost=startup..total (planner units, not ms). rows=estimate. ANALYZE: actual time, actual rows, loops (Nested Loop inner runs loops times — multiply). Huge estimate error → stats. Buffer hits vs reads with BUFFERS. Read inner/leaf nodes first.
