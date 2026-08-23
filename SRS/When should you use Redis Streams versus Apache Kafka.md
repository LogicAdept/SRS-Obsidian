<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/Redis #Messaging/Tools/Kafka #SRS

# When should you use Redis Streams versus Apache Kafka?

> [!abstract] Short answer
> Use **Redis Streams** for **moderate-scale, short-retention** ordered event processing with consumer groups when you **already run Redis** and do not want a separate broker. Use **Apache Kafka** when you need a **dedicated event log** with long retention, very large volume, rich ecosystem (connectors, Kafka Streams), and operational isolation from your cache/session Redis.

## Decision drivers

Redis’s own streaming guide positions Streams as the fit when you need ordered delivery, consumer groups, replay, and bounded retention **without** standing up Kafka/Pulsar — especially for retention windows of **hours or days, not months**, on infrastructure you already operate.

Kafka’s documentation frames the platform as durable event streaming: publish/subscribe, **store events for as long as you want**, process live or retrospectively, with topics whose performance stays effective as data size grows.

| Prefer Redis Streams when… | Prefer Kafka when… |
| --- | --- |
| Redis is already in the stack | You need a central multi-team event hub |
| Retention is short / memory-bounded (`MAXLEN` / `MINID`) | Retention is long or compaction-heavy |
| Latency on the same Redis box matters | Throughput and disk-backed scale dominate |
| Ops cost of a broker is disproportionate | You invest in Kafka clusters, partitions, ACLs |

```d2
direction: right
need: "Ordered events\ngroups + replay" {
  style.fill: "#e3f2fd"
}
redis: "Already have Redis\nshort retention" {
  style.fill: "#e8f5e9"
}
kafka: "Dedicated log\nlong retention / scale" {
  style.fill: "#fff3e0"
}

need -> redis
need -> kafka
```

**Fig. 1.** Same problem shape (streaming); platform choice follows retention, scale, and ops budget.

## Capabilities both offer (differently)

Both support append-only style consumption and consumer-group style work sharing. Redis does it with `XADD` / `XREADGROUP` / `XACK` inside the Redis process. Kafka does it with partitioned topics, consumer groups, and a broker cluster. Spring Data Redis exposes Stream APIs; Spring for Apache Kafka / Kafka Streams cover the Kafka side.

> [!warning] Streams are not “Kafka in Redis memory forever”
> Redis retains stream entries until you trim them; the working set lives in Redis memory (and Redis persistence policies). A log that must outgrow practical Redis size or span months of history is a Kafka (or similar) problem — Redis docs call out dedicated platforms for that weight.

> [!warning] Do not share one Redis for cache + unbounded streams blindly
> Putting a high-volume stream on the same instance as latency-sensitive cache/session data couples failure domains and memory pressure. Kafka isolates the log; Redis Streams share the Redis process.

> [!tip] Interview answer
> I pick Redis Streams for moderate, short-retention event pipelines when Redis is already there — consumer groups and replay without a second platform. I pick Kafka when the event log is a product of its own: long retention, large scale, many consumers, and dedicated ops. Streams are not a drop-in Kafka replacement for unbounded disk-backed logs.

See [[What is the difference between Redis Pub Sub and Redis Streams]], [[How do you implement Redis Pub Sub with Spring Data Redis]], and [[What is RedisTemplate]].
