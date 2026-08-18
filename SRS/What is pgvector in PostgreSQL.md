<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**What is pgvector?**

Extension: vector type + ANN indexes (IVFFlat, HNSW) for embeddings. RAG/search in the same DB. Not a replacement for a dedicated vector DB at huge scale; fine for many product apps. Index build and recall/speed tradeoffs come up in 2026 loops.
