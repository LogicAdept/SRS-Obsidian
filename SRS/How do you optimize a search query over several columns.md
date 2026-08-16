<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**How do you search name OR email OR phone without a seq scan?**

OR across columns often cannot use one B-tree well. UNION ALL of three sargable seeks (each with its own index) can win. Generated tsvector over concatenated fields + GIN. Trigram on a stored concat is usually worse. Avoid WHERE col1||col2 LIKE '%x%'.
