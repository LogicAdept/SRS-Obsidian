<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/Indexes #Databases/Keys #SystemDesign/Performance #SystemDesign/Scalability #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**Point lookup at 1e8 rows?**

B-tree/PK on the int, covering INCLUDE for the payload, keep the row narrow, partition if you also range-scan time. Search-by-text is a different index (trigram/FTS), not another int B-tree.
