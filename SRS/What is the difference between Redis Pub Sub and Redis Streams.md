<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/Redis #SRS

# What is the difference between Redis Pub Sub and Redis Streams?

> [!abstract] Short answer
> **Pub/Sub** is **at-most-once** fire-and-forget fan-out: messages go to **currently subscribed** clients and are discarded — offline subscribers miss them. **Streams** are an **append-only log** with IDs, optional **consumer groups**, **ACK**, and **replay** — better when you need durability and shared work among workers.

## Side-by-side

| | Pub/Sub | Streams |
| --- | --- | --- |
| Model | Channels + live subscribers | Append-only entries (`XADD`) |
| Delivery | At-most-once | At-most-once or at-least-once (with groups/ACK) |
| History / replay | No | Yes (within retention) |
| Consumer groups | No | Yes (`XREADGROUP`, `XACK`) |
| Typical use | Live notifications, cache bust signals | Event pipelines, task-like processing |

Redis docs are explicit: if you need persistence, replay, or stronger delivery, use **Streams**, not Pub/Sub — they solve different problems on the same server.

```java
// Pub/Sub — Spring Data Redis
redis.convertAndSend("orders", payload);

// Streams — template StreamOperations (conceptual)
recordId = redis.opsForStream().add("orders", Map.of("sku", "A1"));
```

**Listing 1.** Publish vs append; Spring Data has first-class Pub/Sub listeners (`RedisMessageListenerContainer` / `@RedisListener`) and Stream APIs on the template.

```d2
direction: right
pub: "PUBLISH channel" {
  style.fill: "#e3f2fd"
}
live: "Online subscribers only" {
  style.fill: "#fff3e0"
}
xadd: "XADD stream" {
  style.fill: "#e8f5e9"
}
log: "Persisted entries\ngroups + ACK" {
  style.fill: "#f3e5f5"
}

pub -> live
xadd -> log
```

**Fig. 1.** Pub/Sub drops messages when nobody is listening; Streams keep an ordered history for consumers to catch up.

## Choosing

Use Pub/Sub for ephemeral fan-out (UI ticks, invalidate-cache broadcasts) where losing a message while a node is down is acceptable. Use Streams when workers must **not** lose work, need **replay**, or share a stream via **consumer groups**. For very large, multi-day retained logs at Kafka scale, teams often still pick a dedicated broker — Streams live in Redis with configurable trimming/retention, not an infinite disk log by default.

> [!warning] Pub/Sub does not queue for late joiners
> A subscriber that connects after `PUBLISH` never sees that message. There is no backlog and no ACK.

> [!warning] Streams still consume Redis memory
> Entries persist until you trim (`MAXLEN` / retention policies) or delete them. Treat capacity and eviction like any other Redis data structure — durability here is not “Kafka on disk forever.”

> [!tip] Interview answer
> Redis Pub/Sub is live at-most-once messaging — great for real-time broadcast, bad if subscribers can be offline. Redis Streams is an append-only log with consumer groups and acknowledgment for reliable processing and replay. Same Redis, different guarantees; Spring Data exposes Pub/Sub listeners and Stream operations on `RedisTemplate`.

See [[How do you implement Redis Pub Sub with Spring Data Redis]], [[When should you use Redis Streams versus Apache Kafka]], and [[What is RedisTemplate]].
