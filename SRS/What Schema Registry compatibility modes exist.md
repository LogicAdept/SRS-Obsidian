<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #DataFormats #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**How does Schema Registry compatibility work when a producer changes a field?**

BACKWARD: new schema reads old data (add optional fields with defaults; do not remove required fields).
FORWARD: old schema reads new data. FULL: both. *_TRANSITIVE applies across all versions. NONE: no check.
Changing a field type is usually rejected. Deploy dance: bump consumers first under BACKWARD, producers first under FORWARD.
