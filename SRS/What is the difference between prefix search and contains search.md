<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**Prefix LIKE vs contains LIKE?**

Prefix 'term%' : B-tree range, cheap, index-friendly. Contains '%term%' : no B-tree seek; need trigram/FTS/external search. Suffix '%term' : reverse(col) indexed as prefix, or trigram. Product search 'contains' is the expensive one — say so on interview.
