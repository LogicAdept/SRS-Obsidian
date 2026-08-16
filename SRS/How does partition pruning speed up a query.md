<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/Partitioning #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**What is partition pruning?**

Planner drops partitions whose bounds cannot match WHERE. Needs a sargable predicate on the partition key (don't wrap it in DATE()). Wrong: WHERE DATE(ts)=. Right: range on ts. EXPLAIN should list only relevant partitions. Not the same as sharding.

**CH partition prune?**

WHERE on the partition key drops whole directories. Still need ORDER BY for inside-partition search. Function-wrapped date can block prune. Check EXPLAIN / selected partitions.
