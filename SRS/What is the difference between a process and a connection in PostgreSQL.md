<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**Why is PostgreSQL process-per-connection?**

Each client backend is an OS process. Simple isolation, expensive fan-out. Hence pooling. Contrast MySQL thread-per-connection. Parallel query uses extra workers (max_parallel_workers).
