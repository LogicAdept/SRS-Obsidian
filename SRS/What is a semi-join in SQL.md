<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**What is a semi-join?**

Keep left rows that have at least one match; do not duplicate left rows. EXISTS / IN (subquery) typically. Unlike INNER JOIN, extra matches do not fan out. Look for Semi Join in EXPLAIN. Use when you only need existence, not child columns.
