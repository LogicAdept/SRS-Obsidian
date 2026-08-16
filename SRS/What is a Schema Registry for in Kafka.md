<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #DataFormats #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**Why Schema Registry?**

BACKWARD: new schema reads old data (add optional fields with defaults; do not remove required fields).
FORWARD: old schema reads new data. FULL: both. *_TRANSITIVE applies across all versions. NONE: no check.
Changing a field type is usually rejected. Deploy dance: bump consumers first under BACKWARD, producers first under FORWARD.

**What are Schema Registry and Avro/Protobuf for?**

Источник: https://habr.com/ru/articles/968844/

Schema Registry хранит схемы и версионирует их. Avro/Protobuf — сериализация по схемам.
