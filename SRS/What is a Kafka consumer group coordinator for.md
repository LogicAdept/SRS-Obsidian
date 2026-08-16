<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Kafka — зачем?**

Распределённый лог-ориентированный брокер. Данные хранятся на диске (retention), не удаляются после прочтения. Topic → Partition → Offset. Partition — единица параллелизма. Зачем: асинхронное взаимодействие, буферизация нагрузки, event sourcing, аудит-лог.

**Consumer Group.**

Каждая партиция — ровно один consumer из группы. Больше партиций → больше параллелизма. Если consumers > partitions — лишние простаивают. Rebalancing при добавлении/падении consumer. Offset commit: auto (рискованно) или manual (контролируемо).

**Как тестировать Kafka в автотесте?**

1) Поднять Kafka через Testcontainers. 2) Отправить сообщение KafkaTemplate.send(topic, message). 3) Прочитать ответное через KafkaConsumer.poll(). 4) Проверить содержимое. Через Citrus: send(kafka).message(...) → receive(kafka).message(...).validate(...). Awaitility для ожидания: await().atMost(5, SECONDS).until(() -> ...).

**Как обеспечить сохранность данных в Kafka?**

replication.factor=3 (каждая партиция на 3 брокерах). min.insync.replicas=2 (минимум 2 реплики подтверждают). acks=all (producer ждёт подтверждения от всех ISR). unclean.leader.election.enable=false (не выбирать лидера из отставших реплик). Если 1 брокер упал — данные не потеряны.

**Kafka — зачем?**

Распределённый лог-ориентированный брокер. Topic → Partition → Offset. Данные не удаляются после прочтения (retention). Асинхронность, буферизация, аудит.

**Consumer Group.**

Каждая партиция — ровно один consumer из группы. Больше партиций → больше параллелизма. Rebalancing при изменении состава.

**What does the group coordinator do?**

A broker elected as coordinator for a group: membership, partition assignment, offset commits to __consumer_offsets. Rebalance is coordinated here. Heartbeats go to the coordinator.

**What does the Kafka Coordinator do in a rebalance?**

Источник: https://habr.com/ru/articles/968844/

Специальный брокер для группы уведомляет консьюмеров о составе группы. Лидер группы получает событие ребаланса (join/leave/падение, смена подписок), считает assignment и рассылает партиции.
