<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/Redis #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Pub/Sub: fire-and-forget, no persistence, no consumer groups, no acknowledgment. If a subscriber is down, messages are lost. Use for ephemeral notifications.

Streams: durable append-only log, consumer groups with acknowledgment, replay from an offset, backpressure. Use for reliable event processing.
> [!warning] Unverified traps from the dump
> - Pub/Sub does not queue missed messages.
> - Streams still live in Redis memory; dumps contrast them with Kafka for large durable logs.
