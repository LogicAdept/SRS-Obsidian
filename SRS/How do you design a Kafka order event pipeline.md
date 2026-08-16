<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #Patterns/Architecture/Microservices #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**Walk through a Kafka architecture for an e-commerce order pipeline.**

Checkout produces to topic orders keyed by orderId (per-order order). Cluster RF=3, acks=all, min.insync.replicas=2. Schema Registry for Avro/JSON schema. Consumer groups: inventory, billing, email — independent offsets. Connect sink to S3/warehouse. Idempotent handlers. DLT for poison events. Lag and URP alerts.

**Kafka plus ClickHouse?**

Kafka engine or ClickPipes → MV → MergeTree/Replacing. At-least-once. ORDER BY (order_id, event_time). Don't use CH as the OLTP source of truth.
