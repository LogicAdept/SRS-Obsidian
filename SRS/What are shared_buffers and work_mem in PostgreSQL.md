<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**Which memory settings matter?**

shared_buffers: shared cache, often ~25% RAM (not 100%; OS cache exists). work_mem: per sort/hash per operation per connection — too high × connections = OOM. maintenance_work_mem for VACUUM/index build. effective_cache_size hints the planner. random_page_cost ~1.1 on SSD.
