<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**Why avoid SELECT * in production?**

Extra I/O, wider rows, cannot Index Only Scan / covering INCLUDE, breaks when columns are added, TOAST fetches for unused fat columns. Name the columns the API needs. SELECT * in EXPLAIN/ad-hoc is fine.
