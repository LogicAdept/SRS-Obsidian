<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**How do you index LIKE '%smith'?**

B-tree on col cannot seek a suffix. Store reverse(col) and query LIKE reverse('%smith') → 'htims%'. Or pg_trgm. Or FTS if it is a word, not a suffix. Don't pretend flipping the user query to 'smith%' is the same predicate.
