<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/Replication #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**What if 10% of customers are 90% of traffic?**

hash(customer_id) hot-spots whales. Options: salt with event_id (queries for one customer hit all shards), dedicated shards for top-N, or more shards. GROUP BY sharding key can skip coordinator merge. Replacing/FINAL needs co-located keys.
