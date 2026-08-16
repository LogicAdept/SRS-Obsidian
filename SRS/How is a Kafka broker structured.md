<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #Messaging/Broker #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**What does a broker store?**

A broker stores partition log segments on disk, serves produce/fetch, hosts leaders and followers. Cluster = many brokers. Controller manages metadata (KRaft quorum or legacy ZK).
