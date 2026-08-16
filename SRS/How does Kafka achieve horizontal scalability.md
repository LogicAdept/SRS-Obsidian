<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SystemDesign/Scalability #DistributedSystems #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**How does Kafka scale horizontally?**

Throughput: partitions are the unit of parallelism. If one partition handles ~X MB/s, need ceil(target/X), then add headroom.
Consumers in a group cannot exceed partition count usefully — extras sit idle.
Ordering: global order needs one partition (throughput cap). Per-key order needs a stable key.
You can add partitions later; you cannot decrease without recreating the topic. Too many partitions cost file handles, leader elections, and metadata.
