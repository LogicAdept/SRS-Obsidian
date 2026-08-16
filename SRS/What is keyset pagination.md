<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/Indexes #SystemDesign/Performance #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**What is keyset / seek / cursor pagination?**

WHERE (created_at, id) < (:ts, :id) ORDER BY created_at DESC, id DESC LIMIT 20. B-tree seeks to the last seen tuple; ~O(page size). Need a unique deterministic order (tie-break with id). Cannot jump to page 873. APIs: after= cursor, not page=50.
