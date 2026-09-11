<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# How do competing consumers work in RabbitMQ

> [!abstract] Short answer
> Several consumers subscribe to the same queue; the broker delivers each message to exactly one of them — round-robin dispatch, gated by each consumer's prefetch. Scale out means adding consumers; the queue is the coordination point, not a shared lock or offset.

## Dispatch mechanics

The queue rotates deliveries across its active consumers in order (round-robin), skipping consumers whose prefetch budget is full — so slow consumers self-throttle while fast ones keep receiving. Processing parallelism is bounded by consumer count times prefetch; a single consumer is a single loop, prefetch only pipelines it. This is RabbitMQ's native work-queue shape and maps directly onto the [[What is the Competing Consumers pattern|competing consumers EIP]].

```d2
direction: down
q: "queue\nround-robin dispatch" {
  width: 240
  height: 80
  style.fill: "#fff3e0"
}
c1: "consumer A" {
  width: 150
  height: 60
  style.fill: "#e3f2fd"
}
c2: "consumer B" {
  width: 150
  height: 60
  style.fill: "#e3f2fd"
}
c3: "consumer C\nprefetch full" {
  width: 180
  height: 60
  style.fill: "#ffebee"
}
q -> c1: "msg 1"
q -> c2: "msg 2"
q -> c3: "skipped (full)"
```

**Fig. 1.** Round-robin skips full consumers, giving natural backpressure without coordination code.

## Where the model bends

Message copy semantics are per queue, not per exchange: two consumer *processes* on one queue split the stream; two *queues* bound to the same exchange each get copies — the pub/sub confusion. Fair dispatch needs tuning: a slow job hogging one consumer with prefetch 1 starves throughput, while a fat prefetch makes one consumer hoard unacked work. If one queue becomes the bottleneck (single queue replica ≈ single core), shard into multiple queues with routing keys or the modulus-hash exchange and keep competing consumers per shard — see [[How do you scale RabbitMQ consumers]].

```java
// two instances, same queue: each message handled once total
ch1.basicConsume("jobs", false, cbA, tag -> {});   // instance A
ch2.basicConsume("jobs", false, cbB, tag -> {});   // instance B
```

**Listing 1.** Competing consumers are just two subscriptions on one queue name — no extra protocol machinery.

> [!warning] One queue is one core
> The docs state a single queue replica is limited to one CPU core on its hot path. Adding consumers cannot push a hot classic or quorum queue past that core; if CPU is the ceiling, the fix is more queues (sharding), not more consumers.

> [!tip] Interview answer
> Competing consumers are multiple subscriptions on one queue with round-robin delivery and per-consumer prefetch throttling: each message goes to exactly one consumer, acks release slots, and scaling is adding processes to the queue. Pub/sub needs separate queues instead, and a saturated queue needs sharding.
