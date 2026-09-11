<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# How is a Kafka consumer structured?

> [!abstract] Short answer
> One `KafkaConsumer` object is a single-threaded engine: a poll loop that fetches from assigned partition leaders, deserializes, and hands you batches; a coordinator client that joins the group and keeps its membership alive; position tracking in memory plus commits to the offsets topic. Under the classic protocol a background heartbeat thread runs the membership liveness; under the new consumer protocol the broker drives it.

## The moving parts

```d2
direction: down
loop: "User poll loop\n(one thread owns the consumer)" {
  width: 300
  height: 90
  style.fill: "#e3f2fd"
}
fetch: "Fetcher\nfetch requests to leaders,\ndeserializers, ConsumerRecords" {
  width: 330
  height: 100
  style.fill: "#e8f5e9"
}
coord: "Coordinator client\njoin/sync, membership liveness" {
  width: 320
  height: 100
  style.fill: "#fff3e0"
}
pos: "Positions\nfetch position in memory,\ncommitted offsets in __consumer_offsets" {
  width: 340
  height: 100
  style.fill: "#f3e5f5"
}
loop -> fetch
loop -> coord
fetch -> pos
```

**Fig. 1.** The consumer is deliberately not concurrent: the loop, the fetcher, and the coordinator client all belong to one thread, which is why `wakeup()` is the only cross-thread call ([[What is the Kafka Consumer API for]]).

The fetcher keeps one or more in-flight fetches per assigned partition leader, applying the fetch size settings and the deserializers; records come back per partition in offset order and the poll call returns them as `ConsumerRecords` ([[How do Kafka consumers fetch messages from a broker]]). The coordinator client talks to the group coordinator broker: it joins, waits for assignment, and maintains membership — under `group.protocol=classic` a background heartbeat thread sends heartbeats at `heartbeat.interval.ms`, while the poll interval is enforced client-side; under the new `consumer` protocol heartbeating is broker-driven and those client knobs disappear ([[What is the Kafka consumer heartbeat thread for]], [[What is a Kafka consumer group coordinator for]]). Positions are two values: the fetch position in memory, and the committed position stored in `__consumer_offsets` via `commitSync`/`commitAsync` ([[What is Kafka Consumer position for]]).

## What the single-thread constraint buys

Because one thread does coordination and fetching, there are no locks on the hot path and no reordering hazards: a batch is assigned, fetched, and delivered in offset order. The cost is the poll-interval contract — all your processing of a `max.poll.records` batch must finish before the next poll or the member is evicted and partitions move ([[What is the difference between session.timeout.ms and max.poll.interval.ms]]). The standard scaling answer is not a shared consumer but many consumers: one per process or one per thread, each with its own group membership, or static members with `group.instance.id` for restart stability ([[What is Kafka static group membership]]). Rebalance callbacks are the only integration point where the consumer calls into your code mid-protocol — commit what you finished before partitions are revoked ([[What triggers a Kafka consumer group rebalance]]).

> [!warning] Deserialization failures kill the loop, not just the record
> The deserializers run inside the consumer on the poll path; a record that cannot be decoded surfaces as an exception in your loop — and if you retry forever from the same offset, the consumer never polls again and the group rebalances on top of you. Skip-or-dead-letter decisions belong in the loop or in a wrapping deserializer, not in an ad-hoc retry ([[How do you handle a poison pill message in Kafka]]).

> [!tip] Interview answer
> A consumer is one thread owning a poll loop: the fetcher pulls batches from partition leaders and deserializes, the coordinator client keeps group membership — heartbeats in the background for the classic protocol, broker-driven for the new one — and positions live in memory until committed to the offsets topic. Single-threaded by contract; scale by adding consumers, and never block the loop past max.poll.interval.ms.

