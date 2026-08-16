<!--
reps: 0
priority: 0
-->
#Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**What is selectivity?**

Selectivity: fraction of rows a predicate matches. High selectivity (few rows) → index seek wins. Low (status='active' on 90%) → seq scan cheaper. Cardinality: distinct values. Histogram/MCV in stats. Boolean columns alone are weak indexes; pair in a composite or use a partial index WHERE flag = true.
