<!--
reps: 0
priority: 0
-->
#Databases/Indexes #SystemDesign/Performance #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**How would you index an admin/search endpoint?**

List actual filters (equality vs range vs text). Equality + sort → composite. Rare flags → partial. Text contains → trigram or FTS, not B-tree. Don't index every combination (write amplification). Unused idx_scan=0. Cover only the columns the list view returns.
