<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**ZooKeeper vs KRaft — что изменилось?**

Старые версии Kafka: ZooKeeper хранил метаданные (контроллер, брокеры, топики). KRaft (Kafka Raft, с Kafka 3.3+): метаданные хранятся в самом Kafka через Raft-консенсус. Проще деплой (нет отдельного ZooKeeper-кластера), быстрее восстановление, меньше точек отказа. ZooKeeper deprecated с Kafka 4.0.

**What is KRaft vs ZooKeeper?**

KRaft stores cluster metadata in Kafka via Raft. No external ZooKeeper. Kafka 3.3+ production path; 4.x removes ZK. Simpler ops, better metadata scale. Interview 2026: greenfield = KRaft.

**What replaced ZooKeeper in Kafka?**

Источник: https://habr.com/ru/articles/968844/

С Kafka 2.8.0 — режим без ZooKeeper (KIP-500). С 3.3+ KRaft (Kafka Raft Metadata Mode) стабилен и рекомендован для новых установок.
