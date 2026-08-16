<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**What is the Kafka controller?**

The controller manages cluster metadata: partition leaders, replica assignment, topic create/delete. In ZooKeeper mode one broker is controller via ZK. In KRaft, a Raft quorum of controllers owns the metadata log. Failure of the active controller fails over inside the quorum.
