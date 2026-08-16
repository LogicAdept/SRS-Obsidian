<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**What is the in-sync replica set (ISR)?**

ISR is the set of replicas that are caught up with the leader (lag below replica.lag.time.max.ms).
acks=all waits for the ISR, not for every replica in the replication factor. A topic can have RF=3 but ISR=1 if followers lag.
If unclean.leader.election.enable=false, only ISR members can become leader. Alert on ISR shrink — durability is gone when ISR=1.
