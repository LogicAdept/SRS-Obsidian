<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SystemDesign/Reliability #DistributedSystems #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**How does Kafka ensure durability?**

ISR is the set of replicas that are caught up with the leader (lag below replica.lag.time.max.ms).
acks=all waits for the ISR, not for every replica in the replication factor. A topic can have RF=3 but ISR=1 if followers lag.
If unclean.leader.election.enable=false, only ISR members can become leader. Alert on ISR shrink — durability is gone when ISR=1.

Follower dies: ISR may shrink; leaders keep serving.
Leader dies: controller elects a new leader from ISR; clients refresh metadata; brief produce/fetch errors.
Too many brokers die: partitions with no ISR leader go offline.
Controller dies: KRaft quorum elects another controller. Use rack awareness so replicas are not all in one AZ.

**How does Kafka provide fault tolerance according to the article?**

Источник: https://habr.com/ru/articles/968844/

Репликация партиций (лидер + N реплик). Запись на лидера, затем репликация; чтение с лидера или реплик (настройки). acks=all — успех после нужного числа реплик. MirrorMaker — резервные кластеры. Контроллер следит за брокерами и выбирает нового лидера.
