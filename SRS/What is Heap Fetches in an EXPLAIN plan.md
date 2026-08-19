<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/Indexes/Covering #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**What do Heap Fetches mean on Index Only Scan?**

Index Only Scan still visited the heap because the visibility map wasn't all-visible. Tune VACUUM; don't assume covering index = no heap I/O. BUFFERS shows the cost.

**Heap Fetches on a covering search?**

Index Only Scan still visited heap (visibility map). VACUUM. SELECT extra unread columns also causes heap I/O even with a 'covering' intent.
