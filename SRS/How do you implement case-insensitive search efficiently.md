<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**How do you search email without LOWER killing the index?**

Don't WHERE LOWER(email) = ? on a plain index. citext type, expression index on lower(email), or store normalized value. ILIKE 'foo%' still needs prefix or trigram. Collation can make comparisons CI but check whether the index uses that collation. Normalize at write time when you can.
