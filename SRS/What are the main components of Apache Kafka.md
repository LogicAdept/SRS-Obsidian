<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из шпаргалок Хабра (MishaBucha, 2025). Не сверен с официальной документацией. Не считать ответом для ревью.

**What are the main Kafka components?**

Источник: https://habr.com/ru/articles/968844/

Broker — хранит и отдаёт сообщения. ZooKeeper — координация брокеров (legacy). С Kafka 2.8 KIP-500 без ZK; с 3.3+ KRaft стабилен и рекомендован. Producer пишет, Consumer читает. Topic — категория. Partition — упорядоченный неизменяемый лог, горизонтальный scale. Consumer Group — набор консьюмеров, вместе читающих топик.
