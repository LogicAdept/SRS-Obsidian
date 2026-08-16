<!--
reps: 0
priority: 0
-->
#Databases/PostgreSQL #Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**What is Index Only Scan and the visibility map?**

If all needed columns are in the index (INCLUDE covering) AND the heap page is all-visible (visibility map bit set by VACUUM), skip heap fetch. Stale VM → heap fetches (Heap Fetches in EXPLAIN). VACUUM is required for IOS to stay cheap.

**IOS for search result lists?**

Index has all columns + VM all-visible. Ideal for typeahead returning id,name from (name) INCLUDE (id). SELECT * or extra joins kill it.
